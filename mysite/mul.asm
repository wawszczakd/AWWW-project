;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 4.0.0 #11528 (Linux)
;--------------------------------------------------------
	MODULE mul
	.optsdcc -mz80
	; Generated using the z80asm/z88 tokens.
	XREF __muluchar_rrx_s
	XREF __mulschar_rrx_s
	XREF __mulint_rrx_s
	XREF __mullong_rrx_s
	XREF __divuchar_rrx_s
	XREF __divschar_rrx_s
	XREF __divsint_rrx_s
	XREF __divuint_rrx_s
	XREF __divulong_rrx_s
	XREF __divslong_rrx_s
	XREF __rrulong_rrx_s
	XREF __rrslong_rrx_s
	XREF __rlulong_rrx_s
	XREF __rlslong_rrx_s

;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	XDEF _main
	XDEF _printf
;--------------------------------------------------------
; Externals used
;--------------------------------------------------------
	XREF _putchar
	XREF _getchar
	XREF _puts
	XREF _vsprintf
	XREF _sprintf
	XREF _vprintf
	XREF _printf
	XREF _printf_small
	XREF __print_format
;--------------------------------------------------------
; special function registers
;--------------------------------------------------------
;--------------------------------------------------------
; ram data
;--------------------------------------------------------
	; Aread BSS
;--------------------------------------------------------
; ram data
;--------------------------------------------------------
	; Area  INITIALIZED
;--------------------------------------------------------
; absolute external ram data
;--------------------------------------------------------
	; Area  DABS (ABS)
;--------------------------------------------------------
; global & static initialisations
;--------------------------------------------------------
	; Area  HOME
	; Area  GSINIT
	; Area  GSFINAL
	; Area  GSINIT
;--------------------------------------------------------
; Home
;--------------------------------------------------------
	; Area HOME
	; Area HOME
;--------------------------------------------------------
; code
;--------------------------------------------------------
	; Area CODE
;mul.c:3: int main() {
;	---------------------------------
; Function main
; ---------------------------------
._main
;mul.c:5: printf("%d\n", a * b);
	ld	hl, $0309
	push	hl
	ld	hl, ___str_0
	push	hl
	call	_printf
	pop	af
	pop	af
;mul.c:6: return 0;
	ld	hl, $0000

.l_main00101
;mul.c:7: }
	ret
___str_0:
	DEFM "%d"
	DEFB $0A
	DEFB $00
	; Area CODE
	; Area  INITIALIZER
	; Area  CABS (ABS)
