// Illustrative millimeter geometry. No physical fit or print approval.
part = "box"; // box, lid, mouth_coupon, rim_coupon
cavity_length = 64;
cavity_width = 44;
cavity_height = 20;
wall = 2;
floor_thickness = 2;
lid_thickness = 2;
rim_wall = 2;
rim_depth = 3;
clearance_per_side = 0.30; // experiment; try 0.15, 0.30, 0.45 separately
coupon_height = 6;
epsilon = 0.01;
outer_length = cavity_length + 2*wall;
outer_width = cavity_width + 2*wall;
rim_length = cavity_length - 2*clearance_per_side;
rim_width = cavity_width - 2*clearance_per_side;
assert(part=="box" || part=="lid" || part=="mouth_coupon" || part=="rim_coupon", "Unknown part");
assert(min(cavity_length,cavity_width,cavity_height,wall,floor_thickness,lid_thickness,rim_wall,rim_depth)>0, "Dimensions must be positive");
assert(clearance_per_side>=0 && min(rim_length,rim_width)>2*rim_wall, "Rim must retain an open center");
assert(coupon_height>=rim_depth && coupon_height<=cavity_height, "Coupon must preserve rim engagement");
module ring(length,width,thickness,height) {
    difference() {
        cube([length,width,height]);
        translate([thickness,thickness,-epsilon]) cube([length-2*thickness,width-2*thickness,height+2*epsilon]);
    }
}
module rim() {
    translate([wall+clearance_per_side,wall+clearance_per_side,0])
        ring(rim_length,rim_width,rim_wall,rim_depth);
}
if (part=="box") difference() {
    cube([outer_length,outer_width,cavity_height+floor_thickness]);
    translate([wall,wall,floor_thickness]) cube([cavity_length,cavity_width,cavity_height+epsilon]);
}
if (part=="lid") union() {
    cube([outer_length,outer_width,lid_thickness]);
    translate([0,0,lid_thickness-epsilon]) scale([1,1,(rim_depth+epsilon)/rim_depth]) rim();
}
if (part=="mouth_coupon") ring(outer_length,outer_width,wall,coupon_height);
// Thin perimeter backing preserves fit while omitting the full lid center.
if (part=="rim_coupon") union() {
    ring(outer_length,outer_width,wall+clearance_per_side+rim_wall,lid_thickness);
    translate([0,0,lid_thickness-epsilon]) scale([1,1,(rim_depth+epsilon)/rim_depth]) rim();
}
