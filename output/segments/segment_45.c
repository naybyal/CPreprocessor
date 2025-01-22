int main(int argc, char *argv[]) {
    // printf("Hello! Breeze is a Text Editor written in C\nPress 'q' to quit!\n\n");
    enableRawMode();
    initEditor();
    if (argc >= 2)
        editorOpen(argv[1]);
    while (1) {
        editorRefreshScreen();
        editorProcessKeypress();
    }
    return 0;
}