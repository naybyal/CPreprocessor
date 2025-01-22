void initEditor() {
    E.cx = 0;
    E.cy = 0;
    E.numrows = 0;
    E.row = NULL;
    E.rowoff = 0;
    E.coloff = 0;
    if (getWindowSize(&E.screenrows, &E.screencols) == -1) 
        die("getWindowSize");
}
