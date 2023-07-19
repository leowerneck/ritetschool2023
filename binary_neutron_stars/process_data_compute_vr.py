from os import mkdir
from os.path import join
from shutil import rmtree
from glob import glob
from multiprocessing import Pool, cpu_count

from matplotlib.pyplot import subplots, pcolormesh, savefig, close
from astropy.constants import G, c, M_sun
from kuibit.simdir import SimDir

outdir = "images_vr"
L = ( G * M_sun / c**2 ).to("km")
T = (L / c).to("ms")

def process_one_iteration(it):
    # Uniform grid parameters
    shape = (401, 401)
    x0    = (-100, -100)
    x1    = (+100, +100)
    # Interpolate vx and vy to a uniform grid
    vx_uniform = vx_all[it].to_UniformGridData(shape, x0, x1)
    vy_uniform = vy_all[it].to_UniformGridData(shape, x0, x1)

    # Get x and y
    x_uniform, y_uniform = vx_uniform.coordinates()

    # Now access the data directly
    t  = vx_all.time_at_iteration(it) * T.value
    x  = x_uniform.data * L.value
    y  = y_uniform.data * L.value
    vx = vx_uniform.data
    vy = vy_uniform.data

    # Compute the radial velocity, adding a small value to r avoid division by zero
    r  = (x**2 + y**2)**0.5 + 1e-30
    vr = (x/r)*vx + (y/r)*vy

    # Create the figure
    fig, ax = subplots(figsize=(4,4))
    im  = pcolormesh(x, y, vr, cmap="bwr", vmin=-1, vmax=1)
    cb  = fig.colorbar(im, label="$v^{r}/c$")
    ax.set_title(f"$t = {t:.2f}$ ms")
    ax.set_xlabel("$x$ [km]")
    ax.set_ylabel("$y$ [km]")
    outfile = join(outdir, f"vr_{it:08d}.png")
    savefig(outfile, dpi=150)
    close(fig)
    print(f"Finished processing iteration {it:08d}. Image saved to '{outfile}'.")

rmtree(outdir, ignore_errors=True)
mkdir(outdir)
for directory in sorted(glob("output_directory_*")):
    print(f"Processing data directory '{directory}'")
    try:
        # Get the data
        sim    = SimDir(directory)
        vx_all = sim.gf.xy["vx"]
        vy_all = sim.gf.xy["vy"]
        its    = vx_all.available_iterations
    except:
        continue

    with Pool(cpu_count()//2) as p:
        p.map(process_one_iteration, its)
