## Stock statement generator
Coding up a transaction statement generator for a trader on stock trading system. Sample data is provided in `input.json` and should produce the exact console output as shown in `output.txt` when run through your program.

## The Data
`actions`: timestamped actions performed by the trader. They can be BUY or SELL actions on any ticker (i.e. while there are only three stocks traded in the input file, this script should work for any ticker so the ticker should not be hardcoded anywhere).

`stock_actions`: the timestamped events that affect a particular stock. They can be stock splits or dividend payouts. Even though these actions are not performed by our trader, they still affect our trader's portfolio, so should be recorded in the statement.
