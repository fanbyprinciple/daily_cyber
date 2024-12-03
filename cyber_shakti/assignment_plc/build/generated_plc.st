PROGRAM assignments
  VAR
    C_1 : BOOL;
  END_VAR
  VAR_OUTPUT
    O_1 : BOOL;
    O_2 : BOOL;
    O_3 : BOOL;
    O_4 : BOOL;
  END_VAR
  VAR
    C_2 : BOOL;
    C_3 : BOOL;
    C_4 : BOOL;
    C_5 : BOOL;
    C_6 : BOOL;
    C_7 : BOOL;
    _TMP_NOT16_OUT : BOOL;
    _TMP_NOT17_OUT : BOOL;
  END_VAR

  _TMP_NOT16_OUT := NOT(NOT(C_2) AND (NOT(C_3) OR c_1));
  O_1 := _TMP_NOT16_OUT;
  O_3 := NOT(C_2) AND (NOT(C_3) OR c_1);
  _TMP_NOT17_OUT := NOT(NOT(C_2) AND (NOT(C_3) OR c_1));
  O_2 := _TMP_NOT17_OUT;
END_PROGRAM


CONFIGURATION Config0

  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#20ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : assignments;
  END_RESOURCE
END_CONFIGURATION
