# Dimensional Engineering

Define nominal dimensions, units, required clearance, fit type, material, orientation, expected shrinkage, elephant-foot risk, hole/XY compensation, and a representative test geometry. Use sliding, loose, snug, friction, press, snap, captive, threaded, bearing, magnet-pocket, NFC-pocket, insert, screw-clearance, or pilot-hole fits deliberately.

Do not prescribe a universal tolerance. Measure the real mating part where possible and use a tolerance coupon or local fit test before a full reprint.


## Calculate the fit before changing geometry

For a mating opening H and insert S in the same units, clearance C = H - S. With limits, worst-case minimum clearance is H_min - S_max and maximum is H_max - S_min. Positive clearance permits space; negative clearance indicates interference. State whether a requested clearance is total/diametral or per side/radial. A 10.00 mm diameter insert with 0.20 mm diametral clearance needs a nominal 10.20 mm opening; 0.20 mm radial clearance implies 10.40 mm. These illustrate arithmetic, not recommended fits.

Record measurement location, tool resolution, repeated readings, material condition, and measurement force for compliant parts. Do not treat displayed decimal places as accuracy. If measurement uncertainty overlaps an acceptance boundary, report an inconclusive result and improve measurement or perform a representative functional fit test before approval.

Keep design allowance, measured process bias, and slicer compensation separate. Change only the appropriate feature when a local hole is wrong; global scaling also changes wall thickness, spacing, and other mating features. Measure several features before attributing a mismatch to scale or shrinkage. For assemblies, calculate the relevant dimension chain and worst-case stack before claiming fit; do not assume independent statistical variation without evidence.

Use a coupon ladder around the measured mate, with labeled candidate clearances and unchanged critical orientation, wall thickness, and engagement length. Record the selected candidate and insertion/removal/retention criterion. A fit coupon does not prove long-term creep, fatigue, temperature performance, or full-part strength.
