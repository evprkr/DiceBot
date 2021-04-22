# /u/_dice_bot
This is a fairly robust dice rolling bot made for Reddit. Invoke it's mighty dice-rolling abilities by calling it's name and giving it a command...

### Basic Usage
Call the bot in the same way you'd call any user, then add your commands inside [brackets], it will ignore any text that is not inside brackets.
See the Formatting section below for more details on how commands work.

Here is an example comment:
`Hey /u/_dice_bot, roll me some dice or something, I need [1d20-1* to hit] and then [2d8 damage] please!`

DiceBot would see the two commands `[1d20-1* to hit]` and `[2d8 damage]`, roll your dice, then reply with something like:
`You rolled [18 (9) to hit] and [12 damage]`

### Formatting Quirks
DiceBot understands certain symbols to mean certain things.

###### Dice
It understands that `d8` and `1d8` mean the same thing.

###### Modifiers
Modifiers can be applied to rolls with `+` or `-`, but modifiers (and all numbers actually) cannot contain decimals.

###### Advantage/Disadvantage
You can roll with advantage or disadvantage by using an asterisk `*` after your die, for example: `[1d20*]`, DiceBot will roll two D20's and return the high and the low rolls formatted as `20 (1)`
