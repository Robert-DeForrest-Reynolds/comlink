# comlink
A utility for communicating with text editors a project's external comments.

Encoding lexographic for comment IDs: `Σ^1 ∪ Σ^2 ∪ Σ^3 ∪ …`

Allows for 1,728,604 unique IDs with 4 characters. So you can represent any comment with 4 characters.

I created the vscode extension to use comlink in vscode, and soon will create a plugin for neovim supporting comlink.

### What is it / What does it do?
 - A described 'protocol' for having a text editor communicate with comlink, allowing anyone to extend their editor to support comlink.
 - Create comments, and are saved into your source code as a comment with an ID. When hovered it will display your comment using the respective text editors tooltip.
 - You can bring comments back into the editor at anytime (implementation dependant on text-editor)

### What is the point?

Because I think documentation, and commenting is important. The thing is, it's incredibly subjective. All comments being there benefits everyone, but everyone personally only needs few comments here and there on things they specifically don't understand.
As well, for incredibly large, and convoluted projects, it could prove very fruitful to have a heavily-detailed documentation embedded within the source files, but bloating the files themselves has always been a problem.

I made comlink to try to solve that problem, and well, just because I wanted to. I find this tool very useful myself, and that's enough to make it.

### Plans
 - Implement a higher ceiling for the unique ID encoding.
 - Neovim plugin
 - Rewrite from Python to C, or implementing in C and creating bindings bare minimum.
 - QoL cleaning utilities for pruning, and reordering.