// Millimeters. Union export for a verified layer-based color change.
// STL carries geometry, not filament assignments or pause commands.
part = "sign"; // sign, coupon
label = "MAKE";
font_name = "Liberation Sans:style=Bold"; // inspect resolved font and all glyphs
letter_size = 16;
base_length = 100;
base_width = 35;
base_thickness = 3;
letter_height = 1;
coupon_length = 40;
coupon_width = 35;
coupon_center_x = 50; // move crop to include critical strokes; do not scale text
coupon_center_y = 17.5;
epsilon = 0.01;
assert(part=="sign" || part=="coupon", "Unknown part");
assert(len(label)>0 && min(letter_size,base_length,base_width,base_thickness,letter_height)>0, "Positive dimensions and nonempty text required");
assert(coupon_length>0 && coupon_width>0 && coupon_length<=base_length && coupon_width<=base_width, "Invalid coupon size");
assert(coupon_center_x>=coupon_length/2 && coupon_center_x<=base_length-coupon_length/2 && coupon_center_y>=coupon_width/2 && coupon_center_y<=base_width-coupon_width/2, "Coupon must lie within base");
// Font metrics vary; clipping is intentional protection against overhanging text.
// Inspect for clipping and missing glyphs before accepting any customized text.
module sign() {
    union() {
        cube([base_length,base_width,base_thickness]);
        intersection() {
            translate([base_length/2,base_width/2,base_thickness-epsilon])
                linear_extrude(height=letter_height+epsilon)
                text(label,size=letter_size,font=font_name,halign="center",valign="center");
            cube([base_length,base_width,base_thickness+letter_height]);
        }
    }
}
if (part=="sign") sign();
if (part=="coupon") intersection() {
    sign();
    translate([coupon_center_x-coupon_length/2,coupon_center_y-coupon_width/2,-epsilon])
        cube([coupon_length,coupon_width,base_thickness+letter_height+2*epsilon]);
}
