#include <ctype.h>
#include <stdio.h>
#include <termios.h>
#include <unistd.h>
#include <stdlib.h>
#include <errno.h>
#include <termios.h>
#include <unistd.h>

/****************** defines *******************/
//The CTRL_KEY macro bitwise-ANDs a character with the value 00011111, in binary. (In C, you generally specify bitmasks using hexadecimal, 
//since C doesn’t have binary literals, and hexadecimal is more concise and readable once you get used to it.)
#define CTRL_KEY(k) ((k) & 0x1f)



/******************* data *******************/


struct editorConfig {
  struct termios orig_termios;
};
struct editorConfig E;

//error handling
void die(const char *s) {
	//clear the screen at exit
	write(STDOUT_FILENO, "\x1b[2J", 4);
  	write(STDOUT_FILENO, "\x1b[H", 3);
	//prints a descriptive error message to stderr.
  	perror(s);
  	//After printing out the error message, we exit the program with an exit status of 1, 
  	//which indicates failure (as would any non-zero value).

  	exit(1);
}



void disableRawMode() {
	//tcsetattr(), tcgetattr(), and read() all return -1 on failure, and set the errno value to indicate the error.
  	if (tcsetattr(STDIN_FILENO, TCSAFLUSH, &E.orig_termios) == -1)
    	die("tcsetattr");
}


/******************* terminal *******************/

//The ECHO feature causes each key you type to be printed to the terminal, so you can see what you’re typing. 
//This is useful in canonical mode, but really gets in the way when we are trying to carefully render a user 
//interface in raw mode. So we turn it off. 
void enableRawMode() {
	//Terminal attributes can be read into a termios struct by tcgetattr().
	 if (tcgetattr(STDIN_FILENO, &E.orig_termios) == -1) die("tcgetattr");
  	//restore their terminal’s original attributes when our program exits.
  	//The atexit() function registers the given function to be called at
    //normal process termination, either via exit(3) or via return from the
    //program's main(). 
  	atexit(disableRawMode);
  	struct termios raw = E.orig_termios;
  	//IXON Turn off Ctrl-S and Ctrl-Q, Now Ctrl-S can be read as a 19 byte and Ctrl-Q can be read as a 17 byte.
  	//ICRNL The I stands for “input flag”, CR stands for “carriage return”, and NL stands for “new line”.
  	//Now Ctrl-M is read as a 13 (carriage return), and the Enter key is also read as a 13.
  	raw.c_iflag &= ~(BRKINT | ICRNL | INPCK | ISTRIP | IXON);
  	raw.c_oflag &= ~(OPOST);
  	//BRKINT, INPCK, ISTRIP, and CS8 all come from <termios.h>.
  	//Those flag probably won’t have any observable effect for you, because these flags are either already turned off, 
  	//or they don’t really apply to modern terminal emulators. 
  	raw.c_cflag |= (CS8);
  	//ECHO is a bitflag, defined as 00000000000000000000000000001000 in binary. 
  	//We use the bitwise-NOT operator (~) on this value to get 11111111111111111111111111110111
  	//ICANON flag allows us to turn off canonical mode.
  	//ISIG -> turn of Ctrl-C and Ctrl-Z: Ctrl-C can be read as a 3 byte and Ctrl-Z can be read as a 26 byte.
  	//IEXTEN -> turn off Ctrl-V and Ctrl-O: Ctrl-V can now be read as a 22 byte, and Ctrl-O as a 15 byte.
  	raw.c_lflag &= ~(ECHO | ICANON | IEXTEN | ISIG);
  	//After modifying them, you can then apply them to the terminal using tcsetattr(). The TCSAFLUSH argument 
  	//specifies when to apply the change: in this case, it waits for all pending output to be written to the terminal
  	//, and also discards any input that hasn’t been read.
  	//The VMIN value sets the minimum number of bytes of input needed before read() can return. 
  	//We set it to 0 so that read() returns as soon as there is any input to be read.
  	raw.c_cc[VMIN] = 0;
  	//VMIN and VTIME come from <termios.h>. 
  	//The VTIME value sets the maximum amount of time to wait before read() returns. 
  	//It is in tenths of a second, so we set it to 1/10 of a second, or 100 milliseconds. If read() times out, it will return 0,
 	raw.c_cc[VTIME] = 10;
 	 if (tcsetattr(STDIN_FILENO, TCSAFLUSH, &raw) == -1) die("tcsetattr");
}




//wait for one keypress, and return it
char editorReadKey() {
  	int nread;
  	char c;
  	//read() and STDIN_FILENO come from <unistd.h>. We are asking read() to read 1 byte 
  	//from the standard input into the variable c, and to keep doing it until there are no more bytes to read. 
  	//read() returns the number of bytes that it read, and will return 0 when it reaches the end of a file.
  	//read: http://gd.tuwien.ac.at/languages/c/programming-bbrown/c_075.htm
  	while ((nread = read(STDIN_FILENO, &c, 1)) != 1) {
    	if (nread == -1 && errno != EAGAIN) die("read");
  	}
  	return c;
}



/*** output ***/

//editorDrawRows() will handle drawing each row of the buffer of text being edited. 
void editorDrawRows() {
  int y;
  for (y = 0; y < 24; y++) {
    write(STDOUT_FILENO, "~\r\n", 3);
  }
}

void editorRefreshScreen() {
	//4 means we are writing 4 bytes out to the terminal
	//The first byte is \x1b, which is the escape character, or 27 in decimal
  	write(STDOUT_FILENO, "\x1b[2J", 4);
  	//H command position the cursor
  	write(STDOUT_FILENO, "\x1b[H", 3);
  	
  	
  editorDrawRows();
  write(STDOUT_FILENO, "\x1b[H", 3);
}




/*** input ***/

void editorProcessKeypress() {
  	char c = editorReadKey();
  	switch (c) {
  		//ASCII value of q is 113(01110001 in binary), CTRL_KEY('q') = 17 which is the ASCII value of CTRL-q
    	case CTRL_KEY('q'):
    		write(STDOUT_FILENO, "\x1b[2J", 4);
      		write(STDOUT_FILENO, "\x1b[H", 3);
      		exit(0);
      		break;
  	}
}



/******************* init *******************/
int main() {
	enableRawMode();
  	
  	
  	while (1) {
  		editorRefreshScreen();
  		editorProcessKeypress();
  	}
  	return 0;
}
