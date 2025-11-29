# Custom scripts

## `disable_bad_blocks_check.sh`

This script disables the kernel's bad blocks checking feature by neutering the
function responsible for it at runtime.

Why would you want to do this? Mainly to allow re-flashing a full NAND image
with OOB data back onto a modem where the OOB data has been corrupted, causing
the blocks to be incorrectly marked as bad.

This allows fully erasing the partition and re-flashing a backup.

## `atc.py`

MicroPython implementation of the `atc` tool to send AT commands to the modem.

## `unlock.bat`

Mysterious batch script found
in [unlock_V7R22_2019-08-11.7z](https://4pda.to/forum/dl/post/26495458/unlock_V7R22_2019-08-11.7z)
that supposedly unlocks the modem. Translated to English.
