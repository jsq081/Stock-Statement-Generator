## The Challenge
Welcome to the stock statement generator! In this problem, you will be coding up a transaction
statement generator for a trader on our stock trading system. Sample data is provided in `input.json` and should produce the exact console output as shown in `output.txt` when run through your program.

## The Data
`actions`: timestamped actions performed by the trader. They can be BUY or SELL actions on any ticker (i.e. while there are only three stocks traded in the input file, this script should work for any ticker so the ticker should not be hardcoded anywhere).

`stock_actions`: the timestamped events that affect a particular stock. They can be stock splits or dividend payouts. Even though these actions are not performed by our trader, they still affect our trader's portfolio, so should be recorded in the statement.

## Your Goal

We are looking for an easy to understand/extend program that doesn't perform any unnecessary actions. You can choose to implement this in whatever language you are most comfortable with. Think of this as a showcase of how you problem solve -- please document (e.g. through commit messages, comments, etc.) any assumptions or decisions you made along the way.
