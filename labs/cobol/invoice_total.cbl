       >>SOURCE FORMAT FREE
identification division.
program-id. invoice-total.
environment division.
configuration section.
repository. function all intrinsic.
data division.
working-storage section.
01 amount-text pic x(32).
01 tax-text pic x(32).
01 gross-amount pic 9(9)v99.
01 tax-percent pic 999v99.
01 final-amount pic 9(10)v99.
01 printed-amount pic z(9)9.99.
procedure division.
    accept amount-text
    accept tax-text
    if test-numval(trim(amount-text)) not = 0
       or test-numval(trim(tax-text)) not = 0
        display "ERROR: numeric inputs required"
        move 1 to return-code
        goback
    end-if
    if numval(amount-text) < 0
       or numval(amount-text) > 999999999.99
       or numval(tax-text) < 0
       or numval(tax-text) > 100
        display "ERROR: amount or tax out of range"
        move 1 to return-code
        goback
    end-if
    compute gross-amount = numval(amount-text)
    compute tax-percent = numval(tax-text)
    compute final-amount rounded =
        gross-amount * (1 + tax-percent / 100)
    move final-amount to printed-amount
    display "TOTAL=" trim(printed-amount)
    move 0 to return-code
    goback.
