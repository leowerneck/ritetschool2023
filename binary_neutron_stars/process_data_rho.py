from os import mkdir
from os.path import join
from shutil import rmtree
from glob import glob
from multiprocessing import Pool, cpu_count

from matplotlib.pyplot import subplots, pcolormesh, savefig, close
from astropy.constants import G, c, M_sun
from kuibit.simdir import SimDir

outdir = "images_rho"
L = ( G * M_sun / c**2 ).to("km")
T = (L / c).to("ms")
D = (M_sun / L**3).to("g/cm3")

def process_one_iteration(it):
    # Uniform grid parameters
    shape = (401, 401)
    x0    = (-100, -100)
    x1    = (+100, +100)
    # Interpolate rho to a uniform grid
    rho_uniform = rho_all[it].to_UniformGridData(shape, x0, x1)

    # Get x and y
    x_uniform, y_uniform = rho_uniform.coordinates()

    # Now access the data directly and convert units
    rho_uniform.data *= D.value
    x   = x_uniform.data * L.value
    y   = y_uniform.data * L.value
    rho = rho_uniform.log10().data

    # Create the figure
    fig, ax = subplots(figsize=(4,4))
    im  = pcolormesh(x, y, rho, cmap="gnuplot", vmin=9, vmax=15)
    cb  = fig.colorbar(im, label=r"$\log_{10}\left(\rho\ [\mathrm{g/cm^{3}}]\right)$")
    ax.set_xlabel(r"$x$ [km]")
    ax.set_ylabel(r"$y$ [km]")
    outfile = join(outdir, f"rho_{it:08d}.png")
    savefig(outfile, dpi=150)
    close(fig)
    print(f"Finished processing iteration {it:08d}. Image saved to '{outfile}'.")

rmtree(outdir, ignore_errors=True)
mkdir(outdir)
for directory in sorted(glob("output_directory_*")):
    print(f"Processing data directory '{directory}'")
    try:
        # Get the data
        sim     = SimDir(directory)
        rho_all = sim.gf.xy["rho_b"]
        its     = rho_all.available_iterations
    except:
        continue

    with Pool(cpu_count()//2) as p:
        p.map(process_one_iteration, its)
