# comlink
A utility for communicating with text editors a project's external comments.

Encoding lexographic for comment IDs: `Σ^1 ∪ Σ^2 ∪ Σ^3 ∪ …`

Allows for 1,728,604 unique IDs with 4 characters. So you can represent any comment with 4 characters.

I created the vscode extension to use comlink in vscode, and soon will create a plugin for neovim supporting comlink.

### What is it / What does it do?
 - A described 'protocol' for having a text editor communicate with comlink, allowing anyone to extend their editor to support comlink.
 - Create comments that are saved into your source code as a comment with an ID. When hovered it will display your comment using the respective text editors tooltip.
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


### comlink <-> editor communication
If you want to create an extension for comlink, or even implement into your text editor, I'll explain how here:<br>
Comlink when running is constantly waiting for input. You tell it what to do by prefixing the data you send it, and it will reply with data with the same prefix.<br>
To tell comlink to load a project's database, you can send `*`.
To send a comment to create, you send the comment prefixed with `~` to comlink, for example: `~some comment`, and the next reply from comlink will be the unique ID for that comment for you to replace the comment text in the editor with. <br>
To get a comment from the database, you send send the ID prefixed with `@` when hovering, for example: `@a2` and the next reply from comlink will be the comment.<br>
To use a comlink command like `init`, you prefix the command with `>`, so you'd send `>init`.<br>

**the editor is responsible for telling comlink:**
 - handling the activation, and parsing requirements
   - `<comment-symbol>~* comment contents ~` turns into `<comment-symbol>id:<id>`
 - when a comment has been created, edited, or deleted
 - what the source file of the comment is
 - what line the comment is on
 - what the comment is

**comlink is responsible for:**
 - tracking id's, and telling the editor what the id of the comment is
 - creating, editing, and removing comments within the database
 - pruning the database
 - managing empty indexes and lost references