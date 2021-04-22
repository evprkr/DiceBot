# DiceBot (aka /u/_dice_bot)
This is a fairly robust dice rolling bot made for Reddit. Invoke it's mighty dice-rolling abilities by calling it's name and giving it a command...

### Basic Usage
Call the bot in the same way you'd call any user, then add your commands inside [brackets], it will ignore any text that is not inside brackets.
See the Formatting section below for more details on how commands work.

Here is an example comment:

`Hey /u/_dice_bot, roll me some dice or something, I need [1d20-1* to hit] and then [2d8 damage] please!`

DiceBot would see the two commands `[1d20-1* to hit]` and `[2d8 damage]`, roll your dice, then reply with something like:

`You rolled [18 (9) to hit] and [12 damage]`

### Formatting Quirks
DiceBot understands certain symbols to mean certain things. Here are all of the formatting rules briefly explained.

##### Basic Die Rules
It understands that `d8` and `1d8` mean the same thing.

##### Roll Modifiers
Modifiers are optional! You don't have to use `1d20+0` to get no modifier. I mean, you can, and DiceBot will do it, it'll just think you're a weirdo.

Modifiers can be applied to rolls with `+` or `-`, but modifiers (and all numbers actually) cannot contain decimals.

##### Advantage/Disadvantage rolls
You can roll with advantage or disadvantage by using an asterisk `*` after your die, for example: `[1d20*]` or `[3d4+1*]`, DiceBot will roll specified dice and return the high and the low rolls formatted as `high (low)` (see the examples in Basic Usage)

##### Roll Labels
This is just for convenience, in case you're rolling a lot of dice in one comment. You can add a label AFTER your roll, and DiceBot will return it along with your roll. See the examples in Basic Usage.

Right now, labels can't contain numbers or special symbols. DiceBot isn't very smart, but we're working on it.

### I AM ERROR
Sometimes DiceBot gets confused, or can't understand the formatting of your commands. As long as you follow the formatting rules, this shouldn't ever happen. However, if it does, DiceBot will let you know something went wrong, and if it's a formatting issue, it'll let you know how to fix it.
If it attempts to roll on a subreddit that it's banned from, it'll send you a DM letting you know what happened, but you'll still get your rolls!
In the event of a Reddit server error, DiceBot will keep trying until it succeeds. Usually server errors only happen for a few seconds at a time.

### Questions, concerns, comments?
Any issues at all can be posted under the Issues section here on the repo. Any comments or concerns, message me on Reddit (/u/Nose_Fetish)

Thanks for using DiceBot!
