// Millimeters. Lightweight desk cable guide only; no load rating.
part = "bracket"; // bracket, fit_coupon
measured_desk_thickness = 20;
clearance_total = 0.4; // experimental TOTAL gap allowance, not per side
arm_thickness = 3;
back_thickness = 3;
engagement = 15;
bracket_width = 25;
coupon_width = 8; // narrower sample does not prove full-width retention
edge_radius = 0.5;
cable_notch_width = 6;
cable_notch_depth = 4;
$fn = 48;
epsilon = 0.01;
gap = measured_desk_thickness + clearance_total;
depth = back_thickness + engagement;
height = gap + 2*arm_thickness;
width = part=="fit_coupon" ? coupon_width : bracket_width;
assert(part=="bracket" || part=="fit_coupon", "Unknown part");
assert(min(measured_desk_thickness,arm_thickness,back_thickness,engagement,bracket_width,coupon_width)>0, "Dimensions must be positive");
assert(clearance_total>=0, "Use a nonnegative trial allowance");
assert(edge_radius>0 && 2*edge_radius<min(arm_thickness,back_thickness), "Edge radius too large");
assert(coupon_width<=bracket_width, "Coupon width exceeds bracket width");
assert(cable_notch_width>0 && cable_notch_width<bracket_width-2*arm_thickness, "Notch must retain side material");
assert(cable_notch_depth>0 && cable_notch_depth<engagement-arm_thickness, "Notch too deep");
module c_profile() {
    offset(r=edge_radius) offset(delta=-edge_radius)
    difference() {
        square([depth,height]);
        translate([back_thickness,arm_thickness]) square([engagement+epsilon,gap]);
    }
}
// C section lies on the bed, width grows vertically.
difference() {
    linear_extrude(height=width) c_profile();
    if (part=="bracket") translate([depth-cable_notch_depth,height-arm_thickness-epsilon,(width-cable_notch_width)/2])
        cube([cable_notch_depth+epsilon,arm_thickness+2*epsilon,cable_notch_width]);
}
