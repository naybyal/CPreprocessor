void editorUpdateRow(erow *row) {
    int j;
    int tabs = 0;
    for (j = 0; j < row->size; j++) { 
        if (row->chars[j] == '\t')
            tabs++;
    }
    free(row->render);
    row->render = malloc(row->size + tabs*(BREEZE_TAB_STOP - 1) + 1);
    int idx = 0;
    for (j = 0; j < row->size; j++) {
        if (row->chars[j] == '\t') {
            row->render[idx++] = ' ';
            while (idx % BREEZE_TAB_STOP != 0)
                row->render[idx++] = ' ';
        }
        else
            row->render[idx++] = row->chars[j];
    }
    row->render[idx] = '\0';
    row->rsize = idx;
}
