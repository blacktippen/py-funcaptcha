If you're solving challenges too fast, ArkoseLabs might start paying attention to what you're doing.

They might utilize one or more of the following tactics to try and stop you:
 
### Harden challenges for the user-agent you're using
In this scenario, the difficulity and volume of challenge images is increased for anybody using the same User-Agent as you.
For example, if you were using a chrome user-agent, everybody using chrome would experience increased difficulity captchas.

This usually doesn't last long, and can be solved by moving to a different User-Agent. (or even better, randomizing them)


### Changes in BDA info
BDA refers to the *bda* parameter in the `/fc/gt2/public_key/` call. It contains fingerprint information about your *browser*.

By default, *py_funcaptcha* attempts to randomize this, but it's possible that ArkoseLabs might do a couple changes here just to mess with you.
