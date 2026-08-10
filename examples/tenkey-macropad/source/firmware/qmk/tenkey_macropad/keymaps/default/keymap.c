#include QMK_KEYBOARD_H

/* Tap Key 10 for F22. Hold Key 10 and press Key 1 to enter the Atmel DFU
 * bootloader. Initial programming and guaranteed recovery remain on AVR ISP. */
const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [0] = LAYOUT_ortho_2x5(
        KC_F13, KC_F14, KC_F15, KC_F16, KC_F17,
        KC_F18, KC_F19, KC_F20, KC_F21, LT(1, KC_F22)
    ),
    [1] = LAYOUT_ortho_2x5(
        QK_BOOT, _______, _______, _______, _______,
        _______, _______, _______, _______, _______
    )
};
