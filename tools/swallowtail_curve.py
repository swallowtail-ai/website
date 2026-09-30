# -*- coding: utf-8 -*-
"""Regenerate the swallowtail curve drawn on the home page.

index.html is hand-maintained; this script exists only to recompute the
<path d="..."> and viewBox if the curve's parameters ever change. Paste the
two printed values into the <svg class="curve"> block.

The curve is the bifurcation set of the swallowtail unfolding: the locus in
(b, c) where V_z = z^4 + a z^2 + b z + c has a repeated root. Placing the
double root at t and solving V_z(t) = V_zz(t) = 0 gives

    b(t) = -4t^3 - 2 a t
    c(t) =  3t^4 +   a t^2

a < 0 gives the self-intersecting shape with two cusps: the swallowtail.
See theorem/swallowtail_theorem.md, Section 10.

    python tools/swallowtail_curve.py
"""
import math

A = -1.0        # unfolding parameter; must be negative for the swallowtail
C_TARGET = 1.5  # how far up the arms run, and so how much of them is shown
N = 260         # samples along the curve
PAD = 16.0      # viewBox padding, in viewBox units
W = 1000.0      # viewBox width


def main():
    T = math.sqrt((-A + math.sqrt(A * A + 12.0 * C_TARGET)) / 6.0)
    pts = []
    for i in range(N + 1):
        t = -T + 2.0 * T * i / N
        pts.append((-4.0 * t ** 3 - 2.0 * A * t, 3.0 * t ** 4 + A * t * t))

    bs = [p[0] for p in pts]
    cs = [p[1] for p in pts]
    bmin, bmax = min(bs), max(bs)
    cmin, cmax = min(cs), max(cs)

    s = (W - 2 * PAD) / (bmax - bmin)
    H = (cmax - cmin) * s + 2 * PAD

    d = []
    for i, (b, c) in enumerate(pts):
        x = PAD + (b - bmin) * s
        y = H - PAD - (c - cmin) * s  # flip c so the tail points down
        d.append(("M" if i == 0 else "L") + "%.1f %.1f" % (x, y))

    print('viewBox="0 0 %.0f %.0f"' % (W, H))
    print()
    print('d="%s"' % " ".join(d))


if __name__ == "__main__":
    main()
