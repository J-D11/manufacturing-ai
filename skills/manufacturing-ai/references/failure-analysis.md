# Failure Analysis

Classify the symptom before assigning a cause: adhesion, warping, extrusion, clog, stringing, blobs, ringing, layer shift, separation, support/bridge failure, surface defect, fit or strength failure, material, AMS, toolhead, sensor, software, network, file, design, or assembly issue.

Separate symptom from cause. Rank causes as confirmed, strongly inferred, possible, or unknown. Choose the smallest diagnostic, make one meaningful change, retest, record the result, and preserve successful settings. For PETG lifting plus stringing, treat adhesion and moisture as separate hypotheses.

When available, compare the failure with the nearest physically successful job under the same machine, tooling, physical surface, material, orientation, and risk geometry. A successful slice is not a physical baseline. Freeze both artifact versions, compare geometry, settings, generated output, machine state, environment, and physical response, and whitelist every intentional delta.

For each rerun, record the baseline, held constants, planned variable, value or behavior actually delivered at the machine, and physical response. If the same failure repeats, stop full production, reopen dependent gates, broaden the hypotheses, and return to a smaller diagnostic.
