from matplotlib import pyplot as plt
import cmocean

from pathlib import Path
import numpy as np
import xarray as xr

from astropy.convolution import Gaussian2DKernel
from astropy.convolution import convolve

# from Projections import x_to_lon_merc, y_to_lat_wmerc


def make_var_image(var,
                   vmin,
                   vmax,
                   cmap='balance',
                   fout=None,
                   orientation='landscape',
                   dpi=120,
                   cbar=True,
                   cbar_kwds={},
                   show_axes=True,
                   grid=False,
                   fig=None,
                   ax=None):
    if cmap in cmocean.cm.cmap_d:
        cmap = cmocean.cm.cmap_d[cmap]

    if ax is None:
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(11, 8))

    Xmin = var.x.data.min()
    Xmax = var.x.data.max()
    Ymin = var.y.data.min()
    Ymax = var.y.data.max()
    extent = (Xmin, Xmax, Ymin, Ymax)
    data = var.data

    if var.y.data[0] < var.y.data[-1]:
        origin = 'lower'
    else:
        origin = 'upper'

    im = ax.imshow(data,
                   vmin=vmin,
                   vmax=vmax,
                   aspect='equal',
                   extent=extent,
                   cmap=cmap,
                   origin=origin)
    if cbar:
        plt.colorbar(im, ax=ax, **cbar_kwds)

    if not show_axes:
        ax.set_axis_off()

    if grid:
        ax.grid()
    ax.set_ylim = (Ymin, Ymax)
    ax.set_xlim = (Xmin, Xmax)

    if fout is not None:
        plt.savefig(fout,
                    orientation=orientation,
                    transparent=True,
                    bbox_inches='tight',
                    pad_inches=0,
                    dpi=dpi)
    return fig, ax


def make_quiver_image(u,
                      v,
                      vmin,
                      vmax,
                      cmap='speed',
                      fout=None,
                      orientation='landscape',
                      dpi=120,
                      cbar=True,
                      cbar_kwds={},
                      show_axes=True,
                      grid=False,
                      subsample=5,
                      width=1.e-3,
                      scale=30,
                      smooth_stddev=None,
                      raster=True,
                      arrows=True,
                      **kwargs):
    if cmap in cmocean.cm.cmap_d:
        cmap = cmocean.cm.cmap_d[cmap]

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(11, 8))

    Xmin = v.x.data.min()
    Xmax = v.x.data.max()
    Ymin = v.y.data.min()
    Ymax = v.y.data.max()
    extent = (Xmin, Xmax, Ymin, Ymax)

    vdata = v.data
    udata = u.data
    speed = np.sqrt(udata**2 + vdata**2)

    if u.y.data[0] < u.y.data[-1]:
        origin = 'lower'
    else:
        origin = 'upper'

    if raster:
        im = ax.imshow(speed,
                       vmin=vmin,
                       vmax=vmax,
                       aspect='equal',
                       extent=extent,
                       cmap=cmap,
                       origin=origin)
        if cbar:
            plt.colorbar(im, ax=ax, **cbar_kwds)

    if smooth_stddev is not None:
        kernel = Gaussian2DKernel(x_stddev=smooth_stddev)
        bad = ~(np.isfinite(udata) & np.isfinite(vdata))
        udata = convolve(udata, kernel)
        udata[bad] = np.nan
        vdata = convolve(vdata, kernel)
        vdata[bad] = np.nan

    if arrows:
        x, y = np.meshgrid(u.x, u.y)
        ax.quiver(x[::subsample, ::subsample],
                  y[::subsample, ::subsample],
                  udata[::subsample, ::subsample],
                  vdata[::subsample, ::subsample],
                  width=width,
                  scale=scale,
                  **kwargs)

    if not show_axes:
        ax.set_axis_off()

    if grid:
        ax.grid()
    ax.set_ylim = (Ymin, Ymax)
    ax.set_xlim = (Xmin, Xmax)

    if fout is not None:
        plt.savefig(fout,
                    orientation=orientation,
                    transparent=True,
                    bbox_inches='tight',
                    pad_inches=0,
                    dpi=dpi)

    return fig, ax


def make_streamplot_image(
        u,
        v,
        vmin,
        vmax,
        cmap='speed',
        fout=None,
        orientation='landscape',
        dpi=120,
        cbar=True,
        cbar_kwds={},
        show_axes=True,
        grid=False,
        subsample=1,
        # width=1.e-3,
        # scale=30,
        smooth_stddev=None,
        raster=True,
        streamlines=True,
        ax=None,
        fig=None,
        **kwargs):
    if not (raster or streamlines):
        raise Exception('(raster or streamlines) must be True')

    if cmap in cmocean.cm.cmap_d:
        cmap = cmocean.cm.cmap_d[cmap]

    if ax is None:
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(11, 8))

    Xmin = v.x.data.min()
    Xmax = v.x.data.max()
    Ymin = v.y.data.min()
    Ymax = v.y.data.max()
    extent = (Xmin, Xmax, Ymin, Ymax)

    y = u.y.data
    x = u.x.data
    vdata = v.data
    udata = u.data
    if u.y.data[0] > u.y.data[-1]:
        y = y[::-1]
        vdata = vdata[::-1, :]
        udata = udata[::-1, :]

    speed = np.sqrt(udata**2 + vdata**2)

    origin = 'lower'

    if raster:
        im = ax.imshow(speed,
                       vmin=vmin,
                       vmax=vmax,
                       aspect='equal',
                       extent=extent,
                       cmap=cmap,
                       origin=origin)
        if cbar:
            plt.colorbar(im, ax=ax, **cbar_kwds)

    if smooth_stddev is not None:
        kernel = Gaussian2DKernel(x_stddev=smooth_stddev)
        bad = ~(np.isfinite(udata) & np.isfinite(vdata))
        udata = convolve(udata, kernel)
        udata[bad] = np.nan
        vdata = convolve(vdata, kernel)
        vdata[bad] = np.nan

    if streamlines:
        x, y = np.meshgrid(x, y)
        ax.streamplot(
            x[::subsample, ::subsample],
            y[::subsample, ::subsample],
            udata[::subsample, ::subsample],
            vdata[::subsample, ::subsample],
            # width=width,
            # scale=scale,
            **kwargs)

    if not show_axes:
        ax.set_axis_off()
    if grid:
        ax.grid()
    ax.set_ylim = (Ymin, Ymax)
    ax.set_xlim = (Xmin, Xmax)

    if fout is not None:
        plt.savefig(fout,
                    orientation=orientation,
                    transparent=True,
                    bbox_inches='tight',
                    pad_inches=0,
                    dpi=dpi)

    return fig, ax


def make_contour_image(
        v,
        vmin,
        vmax,
        cmap='speed',
        fout=None,
        orientation='landscape',
        dpi=120,
        cbar=True,
        cbar_kwds={},
        show_axes=True,
        grid=False,
        subsample=1,
        # width=1.e-3,
        # scale=30,
        smooth_stddev=None,
        raster=True,
        contours=True,
        filled=False,
        fig=None,
        ax=None,
        **kwargs):
    if not (raster or contours):
        raise Exception('(raster or contours) must be True')

    if cmap in cmocean.cm.cmap_d:
        cmap = cmocean.cm.cmap_d[cmap]

    if ax is None:
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(11, 8))

    Xmin = v.x.data.min()
    Xmax = v.x.data.max()
    Ymin = v.y.data.min()
    Ymax = v.y.data.max()
    extent = (Xmin, Xmax, Ymin, Ymax)

    y = v.y.data
    x = v.x.data
    vdata = v.data
    if v.y.data[0] > v.y.data[-1]:
        y = y[::-1]
        vdata = vdata[::-1, :]

    origin = 'lower'

    if raster:
        im = ax.imshow(vdata,
                       vmin=vmin,
                       vmax=vmax,
                       aspect='equal',
                       extent=extent,
                       cmap=cmap,
                       origin=origin)
        if cbar:
            plt.colorbar(im, ax=ax, **cbar_kwds)

    if smooth_stddev is not None:
        kernel = Gaussian2DKernel(x_stddev=smooth_stddev)
        bad = ~np.isfinite(vdata)
        vdata = convolve(vdata, kernel)
        vdata[bad] = np.nan

    if contours:
        x, y = np.meshgrid(x, y)
        if not filled:
            ax.contour(x[::subsample, ::subsample],
                       y[::subsample, ::subsample],
                       vdata[::subsample, ::subsample],
                       vmin=vmin,
                       vmax=vmax,
                       **kwargs)
        else:
            ax.contourf(x[::subsample, ::subsample],
                        y[::subsample, ::subsample],
                        vdata[::subsample, ::subsample],
                        cmap=cmap,
                        vmin=vmin,
                        vmax=vmax,
                        **kwargs)

    if not show_axes:
        ax.set_axis_off()
    if grid:
        ax.grid()
    ax.set_ylim = (Ymin, Ymax)
    ax.set_xlim = (Xmin, Xmax)

    if fout is not None:
        plt.savefig(fout,
                    orientation=orientation,
                    transparent=True,
                    bbox_inches='tight',
                    pad_inches=0,
                    dpi=dpi)

    return fig, ax
