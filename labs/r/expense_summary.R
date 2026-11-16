# Base-R category summary: no third-party package requirements.
summarize_expenses <- function(data) {
  required <- c("category", "amount")
  if (!is.data.frame(data) || !all(required %in% names(data))) {
    stop("Expected columns: category, amount")
  }
  if (anyNA(data[, required]) ||
      !is.numeric(data$amount) ||
      any(!is.finite(data$amount)) ||
      any(data$amount < 0) ||
      any(trimws(as.character(data$category)) == "")) {
    stop("Invalid transaction category or amount")
  }
  if (nrow(data) == 0) {
    return(data.frame(category = character(), total = numeric()))
  }
  totals <- aggregate(amount ~ category, data = data, FUN = sum)
  names(totals)[names(totals) == "amount"] <- "total"
  totals[order(-totals$total, totals$category), , drop = FALSE]
}

if (sys.nframe() == 0) {
  args <- commandArgs(trailingOnly = TRUE)
  if (length(args) != 1) stop("Usage: Rscript expense_summary.R transactions.csv")
  data <- read.csv(args[1], stringsAsFactors = FALSE)
  write.csv(summarize_expenses(data), stdout(), row.names = FALSE)
}
