![image](https://github.com/Hillobar/Rope/assets/63615199/3003777e-1477-4c39-9749-cf2314287cad)

Fork of [Rope](https://github.com/Hillobar/Rope) - software that implements the insightface inswapper_128 model with a helpful GUI.
### [Original author's Discord](https://discord.gg/EcdVAFJzqp)

### [Donate to Hillobar](https://www.paypal.com/donate/?hosted_button_id=Y5SB9LSXFGRF2)

### [Wiki (updated specifically for this repo)](https://github.com/aquawaves/Rope-experimental/wiki)

### Attention, please ###

I am not the author of original software. All rights belong to developers who made all the libraries and scripts required for this software to run.
The main point of it is experimenting with original code and getting new results from existing features, also adding something new.
Main difference: this is the only Linux-compatible fork of Rope, and what do I mean by that is original Rope will work, but you can't change anything in GUI (scroll does not work).

### Even more attention ###

**This software is made for educational and entertainment purposes.**

**None of authors of Rope, Rope-experimental or any libraries/models/scripts included in this project are responsible for user's results from using Rope or any of it's forks.**

Consider ethical usage while running this software. It was not intended to produce any of possible unethical videos or images and authors do not encourage using it this way. Please ask for a person's consent before you use their face for swapping.
For usage of Rope-experimental for research purposes without asking a consent, try using AI-generated faces of unexistent people from this website: [This Person Does Not Exist](https://thispersondoesnotexist.com)

**Huge thanks to [Hillobar](https://github.com/Hillobar) for creating Rope and helping out with bugfixes in EX version.**

### Changelog ###
### Rope EX v24 ###
- Added everything to match new features and bugfixes from latest Rope release. PLEASE NOTICE! Now it requires '-gui' key to start an application.
- Little bit more useful output into console.

### v191123-e3 "Sapphire EX"
- All the bug fixes and features from original Rope's latest update are now there too (added a stop marker, CLIP fixed, better work of enhancers).

### v191123-e2 "Sapphire EX"
- Imported all the features from latest Rope update: some bugfixes and mask view mode.
- Now MouthParser supports values as low as -50 for whole mouth and as high as 50 for mouth & lower lip only. (Works in different direction compared to original Rope)

### v191123 "Sapphire EX"
- Now GUI is fully compatible with Linux-based systems. Models now able to load, scrolling to increase/decrease values now works too.
- Experimental Occluder opacity feature, feel free to test it out.
- Other minor changes that are 100% are here, but I don't remember making them.

### In progress ###

- Providing more useful output into console
- CLI mode

### To do in future versions (no guarantee it will be done): ###
- Adding new enhancer models like GPEN or Real-ESRGAN
- Adding new occluder models
- Unloading models from VRAM for low-end GPU users
