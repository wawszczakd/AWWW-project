;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 4.0.0 #11528 (Linux)
;--------------------------------------------------------
	; MODULE hello_world
	.optsdcc -mz80
	; Generated using the rgbds tokens.
	; We have to define these here as sdcc doesn't make them global by default
	GLOBAL __mulschar
	GLOBAL __muluchar
	GLOBAL __mulint
	GLOBAL __divschar
	GLOBAL __divuchar
	GLOBAL __divsint
	GLOBAL __divuint
	GLOBAL __modschar
	GLOBAL __moduchar
	GLOBAL __modsint
	GLOBAL __moduint
	GLOBAL __mullong
	GLOBAL __modslong
	GLOBAL __divslong
	GLOBAL banked_call
	GLOBAL banked_ret

;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	GLOBAL _main
	GLOBAL _puts
;--------------------------------------------------------
; special function registers
;--------------------------------------------------------
;--------------------------------------------------------
; ram data
;--------------------------------------------------------
	SECTION "hello_world.c_DATA",BSS
;--------------------------------------------------------
; ram data
;--------------------------------------------------------
	SECTION "INITIALIZED",CODE
;--------------------------------------------------------
; absolute external ram data
;--------------------------------------------------------
	SECTION "DABS (ABS)",CODE
;--------------------------------------------------------
; global & static initialisations
;--------------------------------------------------------
	SECTION "HOME",CODE
	SECTION "GSINIT",CODE
	SECTION "GSFINAL",CODE
	SECTION "GSINIT",CODE
;--------------------------------------------------------
; Home
;--------------------------------------------------------
	SECTION "hello_world.c_HOME",HOME
	SECTION "hello_world.c_HOME",HOME
;--------------------------------------------------------
; code
;--------------------------------------------------------
	SECTION "hello_world.c_CODE",CODE
;hello_world.c:3: int main() {
;	---------------------------------
; Function main
; ---------------------------------
_main::
;hello_world.c:4: printf("Hello World!\n");
	ld	hl, ___str_1
	push	hl
	call	_puts
	pop	af
;hello_world.c:5: return 0;
	ld	hl, $0000
.l00101:
;hello_world.c:6: }
	ret
___str_1:
	DB "Hello World!"
	DB $00
	SECTION "hello_world.c_CODE",CODE
	SECTION "INITIALIZER",CODE
	SECTION "CABS (ABS)",CODE
