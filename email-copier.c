/* I use this program as my default email client, because when I try to click
 * email links, often I just want to be able to COPY THE DAMN EMAIL address
 * which is hard to do in thunderbird or mutt.  This just writes them to a text
 * file in my home directory */

#include <stdio.h>

int main(int argc, char** argv) {
    FILE* f = fopen("/home/finlayson/emails.txt", "w");
    for (int i = 1; i < argc; i++) {
        fprintf(f, "%s\n", argv[i]);
    }
    fclose(f);

    return 0;
}

