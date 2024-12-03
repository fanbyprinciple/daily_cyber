#include "beremiz.h"
#ifndef __POUS_H
#define __POUS_H

#include "accessor.h"
#include "iec_std_lib.h"

__DECLARE_ENUMERATED_TYPE(LOGLEVEL,
  LOGLEVEL__CRITICAL,
  LOGLEVEL__WARNING,
  LOGLEVEL__INFO,
  LOGLEVEL__DEBUG
)
// FUNCTION_BLOCK LOGGER
// Data part
typedef struct {
  // FB Interface - IN, OUT, IN_OUT variables
  __DECLARE_VAR(BOOL,EN)
  __DECLARE_VAR(BOOL,ENO)
  __DECLARE_VAR(BOOL,TRIG)
  __DECLARE_VAR(STRING,MSG)
  __DECLARE_VAR(LOGLEVEL,LEVEL)

  // FB private variables - TEMP, private and located variables
  __DECLARE_VAR(BOOL,TRIG0)

} LOGGER;

void LOGGER_init__(LOGGER *data__, BOOL retain);
// Code part
void LOGGER_body__(LOGGER *data__);
// PROGRAM ASSIGNMENTS
// Data part
typedef struct {
  // PROGRAM Interface - IN, OUT, IN_OUT variables
  __DECLARE_VAR(BOOL,O_1)
  __DECLARE_VAR(BOOL,O_2)
  __DECLARE_VAR(BOOL,O_3)
  __DECLARE_VAR(BOOL,O_4)

  // PROGRAM private variables - TEMP, private and located variables
  __DECLARE_VAR(BOOL,C_1)
  __DECLARE_VAR(BOOL,C_2)
  __DECLARE_VAR(BOOL,C_3)
  __DECLARE_VAR(BOOL,C_4)
  __DECLARE_VAR(BOOL,C_5)
  __DECLARE_VAR(BOOL,C_6)
  __DECLARE_VAR(BOOL,C_7)
  __DECLARE_VAR(BOOL,_TMP_NOT16_OUT)
  __DECLARE_VAR(BOOL,_TMP_NOT17_OUT)

} ASSIGNMENTS;

void ASSIGNMENTS_init__(ASSIGNMENTS *data__, BOOL retain);
// Code part
void ASSIGNMENTS_body__(ASSIGNMENTS *data__);
#endif //__POUS_H
