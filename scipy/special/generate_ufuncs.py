#!/usr/bin/python
"""
generate_ufuncs.py

Generate Ufunc definition source files for scipy.special.  Produces
files '_ufuncs.c' and '_ufuncs_cxx.c' by first producing Cython.

This will generate both calls to PyUFunc_FromFuncAndData and the
required ufunc inner loops.

The syntax in the ufunc signature list is

    <line>:           <ufunc_name> '--' <kernels> '--' <headers>
    <kernels>:        <function> [',' <function>]*
    <function>:       <name> ':' <input> '*' <output>
                        '->' <retval> '*' <ignored_retval>
    <input>:          <typecode>*
    <output>:         <typecode>*
    <retval>:         <typecode>?
    <ignored_retval>: <typecode>?
    <headers>:        <header_name> [',' <header_name>]*

The input parameter types are denoted by single character type
codes, according to

   'f': 'float'
   'd': 'double'
   'g': 'long double'
   'F': 'float complex'
   'D': 'double complex'
   'G': 'long double complex'
   'i': 'int'
   'l': 'long'
   'v': 'void'

If multiple kernel functions are given for a single ufunc, the one
which is used is determined by the standard ufunc mechanism. Kernel
functions that are listed first are also matched first against the
ufunc input types, so functions listed earlier take precedence.

In addition, versions with casted variables, such as d->f,D->F and
i->d are automatically generated.

There should be either a single header that contains all of the kernel
functions listed, or there should be one header for each kernel
function. Cython pxd files are allowed in addition to .h files.

"""

#---------------------------------------------------------------------------------
# Ufunc listing
#---------------------------------------------------------------------------------

#
#

# Ufuncs without C++
UFUNCS = """
_lambertw -- lambertw_scalar: Dld->D                       -- lambertw.pxd
_eval_chebyt -- eval_poly_chebyt: ld->d                    -- orthogonal_eval.pxd
logit -- logitf: f->f, logit: d->d, logitl: g->g           -- _logit.h
expit -- expitf: f->f, expit: d->d, expitl: g->g           -- _logit.h
bdtrc -- bdtrc: iid->d                                     -- cephes.h
bdtr -- bdtr: iid->d                                       -- cephes.h
bdtri -- bdtri: iid->d                                     -- cephes.h
btdtr -- btdtr: ddd->d                                     -- cephes.h
btdtri -- incbi: ddd->d                                    -- cephes.h
fdtrc -- fdtrc: ddd->d                                     -- cephes.h
fdtr -- fdtr: ddd->d                                       -- cephes.h
fdtri -- fdtri: ddd->d                                     -- cephes.h
gdtrc -- gdtrc: ddd->d                                     -- cephes.h
gdtr -- gdtr: ddd->d                                       -- cephes.h
hyp2f1 -- hyp2f1: dddd->d, chyp2f1_wrap: dddD->D           -- cephes.h, specfun_wrappers.h
hyp1f1 -- hyp1f1_wrap: ddd->d, chyp1f1_wrap: ddD->D        -- specfun_wrappers.h
hyperu -- hypU_wrap: ddd->d                                -- specfun_wrappers.h
hyp2f0 -- hyp2f0: dddi*d->d                                -- cephes.h
hyp1f2 -- onef2: dddd*d->d                                 -- cephes.h
hyp3f0 -- threef0: dddd*d->d                               -- cephes.h
betainc -- incbet: ddd->d                                  -- cephes.h
betaincinv -- incbi: ddd->d                                -- cephes.h
nbdtrc -- nbdtrc: iid->d                                   -- cephes.h
nbdtr -- nbdtr: iid->d                                     -- cephes.h
nbdtri -- nbdtri: iid->d                                   -- cephes.h
beta -- beta: dd->d                                        -- cephes.h
betaln -- lbeta: dd->d                                     -- cephes.h
cbrt -- cbrt: d->d                                         -- cephes.h
chdtrc -- chdtrc: dd->d                                    -- cephes.h
chdtr -- chdtr: dd->d                                      -- cephes.h
chdtri -- chdtri: dd->d                                    -- cephes.h
dawsn -- dawsn: d->d                                       -- cephes.h
ellipeinc -- ellie: dd->d                                  -- cephes.h
ellipkinc -- ellik: dd->d                                  -- cephes.h
ellipe -- ellpe: d->d                                      -- cephes.h
ellipkm1 -- ellpk: d->d                                    -- cephes.h
exp10 -- exp10: d->d                                       -- cephes.h
exp2 -- exp2: d->d                                         -- cephes.h
gamma -- Gamma: d->d, cgamma_wrap: D->D                    -- cephes.h, specfun_wrappers.h
gammaln -- lgam: d->d, clngamma_wrap: D->D                 -- cephes.h, specfun_wrappers.h
i0 -- i0: d->d                                             -- cephes.h
i0e -- i0e: d->d                                           -- cephes.h
i1 -- i1: d->d                                             -- cephes.h
i1e -- i1e: d->d                                           -- cephes.h
gammaincc -- igamc: dd->d                                  -- cephes.h
gammainc -- igam: dd->d                                    -- cephes.h
gammaincinv -- gammaincinv: dd->d                          -- cephes.h
gammainccinv -- igami: dd->d                               -- cephes.h
iv -- iv: dd->d, cbesi_wrap: dD->D                         -- cephes.h, amos_wrappers.h
ive -- cbesi_wrap_e_real: dd->d, cbesi_wrap_e: dD->D       -- amos_wrappers.h
ellipj -- ellpj: dd*dddd->*i                               -- cephes.h
expn -- expn: id->d                                        -- cephes.h
exp1 -- exp1_wrap: d->d, cexp1_wrap: D->D                  -- specfun_wrappers.h
expi -- expi_wrap: d->d, cexpi_wrap: D->D                  -- specfun_wrappers.h
kn -- kn: id->d                                            -- cephes.h
pdtrc -- pdtrc: id->d                                      -- cephes.h
pdtr -- pdtr: id->d                                        -- cephes.h
pdtri -- pdtri: id->d                                      -- cephes.h
yn -- yn: id->d                                            -- cephes.h
smirnov -- smirnov: id->d                                  -- cephes.h
smirnovi -- smirnovi: id->d                                -- cephes.h
airy -- airy: d*dddd->*i, cairy_wrap: D*DDDD->*i           -- cephes.h, amos_wrappers.h
itairy -- itairy_wrap: d*dddd->*i                          -- specfun_wrappers.h
airye -- cairy_wrap_e_real: d*dddd->*i, cairy_wrap_e: D*DDDD->*i -- amos_wrappers.h
fresnel -- fresnl: d*dd->*i, cfresnl_wrap: D*DD->*i        -- cephes.h, specfun_wrappers.h
shichi -- shichi: d*dd->*i                                 -- cephes.h
sici -- sici: d*dd->*i                                     -- cephes.h
itj0y0 -- it1j0y0_wrap: d*dd->*i                           -- specfun_wrappers.h
it2j0y0 -- it2j0y0_wrap: d*dd->*i                          -- specfun_wrappers.h
iti0k0 -- it1i0k0_wrap: d*dd->*i                           -- specfun_wrappers.h
it2i0k0 -- it2i0k0_wrap: d*dd->*i                          -- specfun_wrappers.h
j0 -- j0: d->d                                             -- cephes.h
y0 -- y0: d->d                                             -- cephes.h
j1 -- j1: d->d                                             -- cephes.h
y1 -- y1: d->d                                             -- cephes.h
jv -- jv: dd->d, cbesj_wrap: dD->D                         -- cephes.h, amos_wrappers.h
jve -- cbesj_wrap_e_real: dd->d, cbesj_wrap_e: dD->D       -- amos_wrappers.h
yv -- yv: dd->d, cbesy_wrap: dD->D                         -- cephes.h, amos_wrappers.h
yve -- cbesy_wrap_e_real: dd->d, cbesy_wrap_e: dD->D       -- amos_wrappers.h
k0 -- k0: d->d                                             -- cephes.h
k0e -- k0e: d->d                                           -- cephes.h
k1 -- k1: d->d                                             -- cephes.h
k1e -- k1e: d->d                                           -- cephes.h
kv -- cbesk_wrap_real: dd->d, cbesk_wrap: dD->D            -- amos_wrappers.h
kve -- cbesk_wrap_e_real: dd->d, cbesk_wrap_e: dD->D       -- amos_wrappers.h
hankel1 -- cbesh_wrap1: dD->D                              -- amos_wrappers.h
hankel1e -- cbesh_wrap1_e: dD->D                           -- amos_wrappers.h
hankel2 -- cbesh_wrap2: dD->D                              -- amos_wrappers.h
hankel2e -- cbesh_wrap2_e: dD->D                           -- amos_wrappers.h
ndtr -- ndtr: d->d                                         -- cephes.h
log_ndtr -- log_ndtr: d->d                                 -- cephes.h
erfc -- erfc: d->d                                         -- cephes.h
erf -- erf: d->d, cerf_wrap: D->D                          -- cephes.h, specfun_wrappers.h
ndtri -- ndtri: d->d                                       -- cephes.h
psi -- psi: d->d, cpsi_wrap: D->D                          -- cephes.h, specfun_wrappers.h
rgamma -- rgamma: d->d, crgamma_wrap: D->D                 -- cephes.h, specfun_wrappers.h
round -- round: d->d                                       -- cephes.h
sindg -- sindg: d->d                                       -- cephes.h
cosdg -- cosdg: d->d                                       -- cephes.h
radian -- radian: ddd->d                                   -- cephes.h
tandg -- tandg: d->d                                       -- cephes.h
cotdg -- cotdg: d->d                                       -- cephes.h
log1p -- log1p: d->d                                       -- cephes.h
expm1 -- expm1: d->d                                       -- cephes.h
cosm1 -- cosm1: d->d                                       -- cephes.h
spence -- spence: d->d                                     -- cephes.h
zetac -- zetac: d->d                                       -- cephes.h
struve -- struve_wrap: dd->d                               -- specfun_wrappers.h
modstruve -- modstruve_wrap: dd->d                         -- specfun_wrappers.h
itstruve0 -- itstruve0_wrap: d->d                          -- specfun_wrappers.h
it2struve0 -- it2struve0_wrap: d->d                        -- specfun_wrappers.h
itmodstruve0 -- itmodstruve0_wrap: d->d                    -- specfun_wrappers.h
kelvin -- kelvin_wrap: d*DDDD->*i                          -- specfun_wrappers.h
ber -- ber_wrap: d->d                                      -- specfun_wrappers.h
bei -- bei_wrap: d->d                                      -- specfun_wrappers.h
ker -- ker_wrap: d->d                                      -- specfun_wrappers.h
kei -- kei_wrap: d->d                                      -- specfun_wrappers.h
berp -- berp_wrap: d->d                                    -- specfun_wrappers.h
beip -- beip_wrap: d->d                                    -- specfun_wrappers.h
kerp -- kerp_wrap: d->d                                    -- specfun_wrappers.h
keip -- keip_wrap: d->d                                    -- specfun_wrappers.h
zeta -- zeta: dd->d                                        -- cephes.h
kolmogorov -- kolmogorov: d->d                             -- cephes.h
kolmogi -- kolmogi: d->d                                   -- cephes.h
besselpoly -- besselpoly: ddd->d                           -- c_misc/misc.h
btdtria -- cdfbet3_wrap: ddd->d                            -- cdf_wrappers.h
btdtrib -- cdfbet4_wrap: ddd->d                            -- cdf_wrappers.h
bdtrik -- cdfbin2_wrap: ddd->d                             -- cdf_wrappers.h
bdtrin -- cdfbin3_wrap: ddd->d                             -- cdf_wrappers.h
chdtriv -- cdfchi3_wrap: dd->d                             -- cdf_wrappers.h
chndtr -- cdfchn1_wrap: ddd->d                             -- cdf_wrappers.h
chndtrix -- cdfchn2_wrap: ddd->d                           -- cdf_wrappers.h
chndtridf -- cdfchn3_wrap: ddd->d                          -- cdf_wrappers.h
chndtrinc -- cdfchn4_wrap: ddd->d                          -- cdf_wrappers.h
fdtridfd -- cdff4_wrap: ddd->d                             -- cdf_wrappers.h
ncfdtr -- cdffnc1_wrap: dddd->d                            -- cdf_wrappers.h
ncfdtri -- cdffnc2_wrap: dddd->d                           -- cdf_wrappers.h
ncfdtridfn -- cdffnc3_wrap: dddd->d                        -- cdf_wrappers.h
ncfdtridfd -- cdffnc4_wrap: dddd->d                        -- cdf_wrappers.h
ncfdtrinc -- cdffnc5_wrap: dddd->d                         -- cdf_wrappers.h
gdtrix -- cdfgam2_wrap: ddd->d                             -- cdf_wrappers.h
gdtrib -- cdfgam3_wrap: ddd->d                             -- cdf_wrappers.h
gdtria -- cdfgam4_wrap: ddd->d                             -- cdf_wrappers.h
nbdtrik -- cdfnbn2_wrap: ddd->d                            -- cdf_wrappers.h
nbdtrin -- cdfnbn3_wrap: ddd->d                            -- cdf_wrappers.h
nrdtrimn -- cdfnor3_wrap: ddd->d                           -- cdf_wrappers.h
nrdtrisd -- cdfnor4_wrap: ddd->d                           -- cdf_wrappers.h
pdtrik -- cdfpoi2_wrap: dd->d                              -- cdf_wrappers.h
stdtr -- cdft1_wrap: dd->d                                 -- cdf_wrappers.h
stdtrit -- cdft2_wrap: dd->d                               -- cdf_wrappers.h
stdtridf -- cdft3_wrap: dd->d                              -- cdf_wrappers.h
nctdtr -- cdftnc1_wrap: ddd->d                             -- cdf_wrappers.h
nctdtrit -- cdftnc2_wrap: ddd->d                           -- cdf_wrappers.h
nctdtridf -- cdftnc3_wrap: ddd->d                          -- cdf_wrappers.h
nctdtrinc -- cdftnc4_wrap: ddd->d                          -- cdf_wrappers.h
tklmbda -- tukeylambdacdf: dd->d                           -- cdf_wrappers.h
mathieu_a -- cem_cva_wrap: dd->d                           -- specfun_wrappers.h
mathieu_b -- sem_cva_wrap: dd->d                           -- specfun_wrappers.h
mathieu_cem -- cem_wrap: ddd*dd->*i                        -- specfun_wrappers.h
mathieu_sem -- sem_wrap: ddd*dd->*i                        -- specfun_wrappers.h
mathieu_modcem1 -- mcm1_wrap: ddd*dd->*i                   -- specfun_wrappers.h
mathieu_modcem2 -- mcm2_wrap: ddd*dd->*i                   -- specfun_wrappers.h
mathieu_modsem1 -- msm1_wrap: ddd*dd->*i                   -- specfun_wrappers.h
mathieu_modsem2 -- msm2_wrap: ddd*dd->*i                   -- specfun_wrappers.h
lpmv -- pmv_wrap: ddd->d                                   -- specfun_wrappers.h
pbwa -- pbwa_wrap: dd*dd->*i                               -- specfun_wrappers.h
pbdv -- pbdv_wrap: dd*dd->*i                               -- specfun_wrappers.h
pbvv -- pbvv_wrap: dd*dd->*i                               -- specfun_wrappers.h
pro_cv -- prolate_segv_wrap: ddd->d                        -- specfun_wrappers.h
obl_cv -- oblate_segv_wrap: ddd->d                         -- specfun_wrappers.h
pro_ang1_cv -- prolate_aswfa_wrap: ddddd*dd->*i            -- specfun_wrappers.h
pro_rad1_cv -- prolate_radial1_wrap: ddddd*dd->*i          -- specfun_wrappers.h
pro_rad2_cv -- prolate_radial2_wrap: ddddd*dd->*i          -- specfun_wrappers.h
obl_ang1_cv -- oblate_aswfa_wrap: ddddd*dd->*i             -- specfun_wrappers.h
obl_rad1_cv -- oblate_radial1_wrap: ddddd*dd->*i           -- specfun_wrappers.h
obl_rad2_cv -- oblate_radial2_wrap: ddddd*dd->*i           -- specfun_wrappers.h
pro_ang1 -- prolate_aswfa_nocv_wrap: dddd*d->d             -- specfun_wrappers.h
pro_rad1 -- prolate_radial1_nocv_wrap: dddd*d->d           -- specfun_wrappers.h
pro_rad2 -- prolate_radial2_nocv_wrap: dddd*d->d           -- specfun_wrappers.h
obl_ang1 -- oblate_aswfa_nocv_wrap: dddd*d->d              -- specfun_wrappers.h
obl_rad1 -- oblate_radial1_nocv_wrap: dddd*d->d            -- specfun_wrappers.h
obl_rad2 -- oblate_radial2_nocv_wrap: dddd*d->d            -- specfun_wrappers.h
modfresnelp -- modified_fresnel_plus_wrap: d*DD->*i        -- specfun_wrappers.h
modfresnelm -- modified_fresnel_minus_wrap: d*DD->*i       -- specfun_wrappers.h
"""

# Ufuncs with C++
UFUNCS_CXX = """
wofz -- wofz: D->D                                         -- _faddeeva.pxd
"""

#---------------------------------------------------------------------------------
# Extra code
#---------------------------------------------------------------------------------

EXTRA_CODE_COMMON = """
#
# Error handling system
#

cdef extern from "stdarg.h":
     ctypedef struct va_list:
         pass
     ctypedef struct fake_type:
         pass
     void va_start(va_list, void* arg) nogil
     void* va_arg(va_list, fake_type) nogil
     void va_end(va_list) nogil
     fake_type int_type "int"

cdef extern from "Python.h":
    int PyOS_vsnprintf(char *, size_t, char *, va_list va) nogil

from cpython.exc cimport PyErr_WarnEx

cdef public void scipy_special_raise_warning(char *fmt, ...) nogil except *:
    cdef char msg[1024]
    cdef va_list ap

    va_start(ap, fmt)
    PyOS_vsnprintf(msg, 1024, fmt, ap)
    va_end(ap)

    with gil:
        from scipy.special import SpecialFunctionWarning
        PyErr_WarnEx(SpecialFunctionWarning, msg, 1)

def _errprint(inflag=None):
    \"\"\"
    errprint(flag)

    Sets the error printing flag for special functions (from the
    cephesmodule). The output is the previous state.  With errprint(0)
    no error messages are shown; the default is errprint(1).  If no
    argument is given the current state of the flag is returned and no
    change occurs.

    \"\"\"
    global scipy_special_print_error_messages
    cdef int oldflag

    oldflag = scipy_special_print_error_messages
    if inflag is not None:
        scipy_special_print_error_messages = int(bool(inflag))

    return oldflag

"""

EXTRA_CODE = EXTRA_CODE_COMMON + """
cdef extern int scipy_special_print_error_messages

#
# Aliases
#

jn = jv
"""

EXTRA_CODE_CXX = EXTRA_CODE_COMMON + """
cdef public int scipy_special_print_error_messages
"""



#---------------------------------------------------------------------------------
# Code generation
#---------------------------------------------------------------------------------

import subprocess
import optparse
import re
import textwrap
import add_newdocs

CY_TYPES = {
    'f': 'float',
    'd': 'double',
    'g': 'long double',
    'F': 'float complex',
    'D': 'double complex',
    'G': 'long double complex',
    'i': 'int',
    'l': 'long',
    'v': 'void',
}

C_TYPES = {
    'f': 'np.npy_float',
    'd': 'np.npy_double',
    'g': 'np.npy_longdouble',
    'F': 'np.npy_cfloat',
    'D': 'np.npy_cdouble',
    'G': 'np.npy_clongdouble',
    'i': 'np.npy_int',
    'l': 'np.npy_long',
    'v': 'void',
}

TYPE_NAMES = {
    'f': 'np.NPY_FLOAT',
    'd': 'np.NPY_DOUBLE',
    'g': 'np.NPY_LONGDOUBLE',
    'F': 'np.NPY_CFLOAT',
    'D': 'np.NPY_CDOUBLE',
    'G': 'np.NPY_CLONGDOUBLE',
    'i': 'np.NPY_INT',
    'l': 'np.NPY_LONG',
}

def generate_loop(func_inputs, func_outputs, func_retval,
                  ufunc_inputs, ufunc_outputs):
    """
    Generate a UFunc loop function that calls a function given as its
    data parameter with the specified input and output arguments and
    return value.

    This function can be passed to PyUFunc_FromFuncAndData.

    Parameters
    ----------
    func_inputs, func_outputs, func_retval : str
        Signature of the function to call, given as type codes of the
        input, output and return value arguments. These 1-character
        codes are given according to the CY_TYPES and TYPE_NAMES
        lists above.

        The corresponding C function signature to be called is:

            retval func(intype1 iv1, intype2 iv2, ..., outtype1 *ov1, ...);

        If len(func_outputs) == len(ufunc_outputs)+1, the return value
        is treated as the first output argument. Otherwise, the return
        value is ignored.

    ufunc_inputs, ufunc_outputs : str
        Ufunc input and output signature.

        This does not have to exactly match the function signature,
        as long as the type casts work out on the C level.

    Returns
    -------
    loop_name
        Name of the generated loop function.
    loop_body
        Generated C code for the loop.

    """
    if len(func_inputs) != len(ufunc_inputs):
        raise ValueError("Function and ufunc have different number of inputs")

    if len(func_outputs) != len(ufunc_outputs) and not (
            func_retval != "v" and len(func_outputs)+1 == len(ufunc_outputs)):
        raise ValueError("Function retval and ufunc outputs don't match")

    name = "loop_%s_%s_%s_As_%s_%s" % (
        func_retval, func_inputs, func_outputs, ufunc_inputs, ufunc_outputs
        )
    body = "cdef void %s(char **args, np.npy_intp *dims, np.npy_intp *steps, void *func) nogil:\n" % name
    body += "    cdef np.npy_intp i, n = dims[0]\n"

    pointers = []
    for j in range(len(ufunc_inputs)):
        pointers.append("*ip%d = args[%d]" % (j, j))
    for j in range(len(ufunc_outputs)):
        pointers.append("*op%d = args[%d]" % (j, j + len(ufunc_inputs)))
    body += "    cdef char %s\n" % ", ".join(pointers)

    ftypes = []
    fvars = []
    outtypecodes = []
    for j in range(len(func_inputs)):
        ftypes.append(CY_TYPES[func_inputs[j]])
        fvars.append("<%s>(<%s*>ip%d)[0]" % (
            CY_TYPES[func_inputs[j]],
            CY_TYPES[ufunc_inputs[j]], j))

    if len(func_outputs)+1 == len(ufunc_outputs):
        func_joff = 1
        outtypecodes.append(func_retval)
        body += "    cdef %s ov0\n" % (CY_TYPES[func_retval],)
    else:
        func_joff = 0

    for j, outtype in enumerate(func_outputs):
        body += "    cdef %s ov%d\n" % (CY_TYPES[outtype], j+func_joff)
        ftypes.append("%s *" % CY_TYPES[outtype])
        fvars.append("&ov%d" % (j+func_joff))
        outtypecodes.append(outtype)

    body += "    for i in range(n):\n"
    if len(func_outputs)+1 == len(ufunc_outputs):
        rv = "ov0 = "
    else:
        rv = ""

    body += "        %s(<%s(*)(%s) nogil>func)(%s)\n" % (
        rv, CY_TYPES[func_retval],
        ", ".join(ftypes), ", ".join(fvars))

    for j, (outtype, fouttype) in enumerate(zip(ufunc_outputs, outtypecodes)):
        body += "        (<%s *>op%d)[0] = <%s>ov%d\n" % (
            CY_TYPES[outtype], j, CY_TYPES[outtype], j)
    for j in range(len(ufunc_inputs)):
        body += "        ip%d += steps[%d]\n" % (j, j)
    for j in range(len(ufunc_outputs)):
        body += "        op%d += steps[%d]\n" % (j, j + len(ufunc_inputs))

    return name, body

def iter_variants(inputs, outputs):
    """
    Generate variants of UFunc signatures, by changing variable types,
    within the limitation that the corresponding C types casts still
    work out.

    This does not generate all possibilities, just the ones required
    for the ufunc to work properly with the most common data types.

    Parameters
    ----------
    inputs, outputs : str
        UFunc input and output signature strings

    Yields
    ------
    new_input, new_output : str
        Modified input and output strings.
        Also the original input/output pair is yielded.

    """
    maps = [
        # always use long instead of int (more common type on 64-bit)
        ('i', 'l'),
    ]

    # allow doubles in integer args
    if 'd' in inputs+outputs or 'D' in inputs+outputs:
        maps.append(('il', 'dd'))
    if 'f' in inputs+outputs or 'F' in inputs+outputs:
        maps.append(('il', 'ff'))

    # float32-preserving signatures
    maps = [(a + 'dD', b + 'fF') for a, b in maps] + maps

    # do the replacements
    for src, dst in maps:
        new_inputs = inputs
        new_outputs = outputs
        for a, b in zip(src, dst):
            new_inputs = new_inputs.replace(a, b)
            new_outputs = new_outputs.replace(a, b)
        yield new_inputs, new_outputs

class Ufunc(object):
    """
    Ufunc signature, restricted format suitable for special functions.

    Parameters
    ----------
    name
        Name of the ufunc to create
    signature
        String of form 'func: fff*ff->f, func2: ddd->*i' describing
        the C-level functions and types of their input arguments
        and return values.

        The syntax is 'function_name: inputparams*outputparams->output_retval*ignored_retval'

    """
    def __init__(self, name, signatures):
        self.name = name
        self.signatures = self._parse_signatures(signatures)
        self.doc = add_newdocs.get("scipy.special." + name)
        if self.doc is None:
            raise ValueError("No docstring for ufunc %r" % name)
        self.doc = textwrap.dedent(self.doc).strip()

    def _parse_signatures(self, sigs):
        return [self._parse_signature(x) for x in sigs.split(",")
                if x.strip()]

    def _parse_signature(self, sig):
        m = re.match("\s*(.*):\s*([fdgFDGil]*)\s*\\*\s*([fdgFDGil]*)\s*->\s*([*fdgFDGil]*)\s*$", sig)
        if m:
            func, inarg, outarg, ret = map(lambda x: x.strip(), m.groups())
            if ret.count('*') > 1:
                raise ValueError("%s: Invalid signature: %r" % (self.name, sig))
            return (func, inarg, outarg, ret)
        m = re.match("\s*(.*):\s*([fdgFDGil]*)\s*->\s*([fdgFDGil]?)\s*$", sig)
        if m:
            func, inarg, ret = map(lambda x: x.strip(), m.groups())
            return (func, inarg, "", ret)
        raise ValueError("%s: Invalid signature: %r" % (self.name, sig))

    def _get_signatures_and_loops(self, all_loops):
        inarg_num = None
        outarg_num = None

        seen = set()
        variants = []

        def add_variant(func_name, inarg, outarg, ret, inp, outp):
            if (inp, outp) in seen:
                return
            seen.add((inp, outp))

            sig = (func_name, inp, outp)
            if "v" in outp:
                raise ValueError("%s: void signature %r" % (self.name, sig))
            if len(inp) != inarg_num or len(outp) != outarg_num:
                raise ValueError("%s: signature %r does not have %d/%d input/output args" % (
                    self.name, sig,
                    inarg_num, outarg_num))

            loop_name, loop = generate_loop(inarg, outarg, ret, inp, outp)
            all_loops[loop_name] = loop
            variants.append((func_name, loop_name, inp, outp))

        for func_name, inarg, outarg, ret in self.signatures:
            outp = re.sub(r'\*.*', '', ret) + outarg
            ret = ret.replace('*', '')
            if inarg_num is None:
                inarg_num = len(inarg)
                outarg_num = len(outp)
            for inp2, outp2 in iter_variants(inarg, outp):
                add_variant(func_name, inarg, outarg, ret, inp2, outp2)
        return variants, inarg_num, outarg_num

    def get_prototypes(self):
        prototypes = []
        for func_name, inarg, outarg, ret in self.signatures:
            ret = ret.replace('*', '')
            c_args = ([C_TYPES[x] for x in inarg]
                      + [C_TYPES[x] + ' *' for x in outarg])
            cy_args = ([CY_TYPES[x] for x in inarg]
                       + [CY_TYPES[x] + ' *' for x in outarg])
            c_proto = "%s (*)(%s)" % (C_TYPES[ret], ", ".join(c_args))
            cy_proto = "%s (*)(%s)" % (CY_TYPES[ret], ", ".join(cy_args))
            prototypes.append((func_name, c_proto, cy_proto))
        return prototypes

    def generate(self, all_loops):
        toplevel = ""

        variants, inarg_num, outarg_num = self._get_signatures_and_loops(all_loops)

        loops = []
        datas = []
        types = []

        for func_name, loop_name, inputs, outputs in variants:
            for x in inputs:
                types.append(TYPE_NAMES[x])
            for x in outputs:
                types.append(TYPE_NAMES[x])
            loops.append(loop_name)
            datas.append(func_name)

        toplevel += "cdef np.PyUFuncGenericFunction ufunc_%s_loops[%d]\n" % (self.name, len(loops))
        toplevel += "cdef void *ufunc_%s_data[%d]\n" % (self.name, len(datas))
        toplevel += "cdef char ufunc_%s_types[%d]\n" % (self.name, len(types))
        toplevel += 'cdef char *ufunc_%s_doc = (\n    "%s")\n' % (
            self.name,
            self.doc.replace('"', '\\"').replace('\n', '\\n\"\n    "')
            )

        for j, function in enumerate(loops):
            toplevel += "ufunc_%s_loops[%d] = <np.PyUFuncGenericFunction>%s\n" % (self.name, j, function)
        for j, type in enumerate(types):
            toplevel += "ufunc_%s_types[%d] = <char>%s\n" % (self.name, j, type)
        for j, data in enumerate(datas):
            toplevel += "ufunc_%s_data[%d] = <void*>_func_%s\n" % (self.name, j, data)

        toplevel += ('@ = np.PyUFunc_FromFuncAndData(ufunc_@_loops, '
                     'ufunc_@_data, ufunc_@_types, %d, %d, %d, 0, '
                     '"@", ufunc_@_doc, 0)\n' % (len(types)/(inarg_num+outarg_num),
                                                 inarg_num, outarg_num)
                     ).replace('@', self.name)

        return toplevel

def generate(filename, ufunc_str, extra_code):
    ufuncs = []
    headers = {}

    lines = ufunc_str.splitlines()
    lines.sort()

    for line in lines:
        line = line.strip()
        if not line:
            continue
        m = re.match("^([a-z0-9_]+)\s*--\s*(.*?)\s*(--.*)?$", line)
        if not m:
            raise ValueError("Unparseable line %r" % line)
        ufuncs.append(Ufunc(m.group(1), m.group(2)))
        if m.group(3):
            headers[ufuncs[-1].name] = [x.strip() for x in m.group(3)[2:].split(",")]

    toplevel = ""
    defs = ""
    all_loops = {}

    ufuncs.sort(key=lambda u: u.name)
    for ufunc in ufuncs:
        t = ufunc.generate(all_loops)
        toplevel += t + "\n"

        cfuncs = ufunc.get_prototypes()

        hdrs = headers.get(ufunc.name, ['cephes.h'])
        if len(hdrs) == 1:
            hdrs = [hdrs[0]] * len(cfuncs)
        elif len(hdrs) != len(cfuncs):
            raise ValueError("%s: wrong number of headers" % ufunc.name)

        for (c_name, c_proto, cy_proto), header in zip(cfuncs, hdrs):
            if header.endswith('.pxd'):
                defs += "from %s cimport %s as _func_%s\n" % (header[:-4], c_name, c_name)

                # check function signature at compile time
                proto_name = '_proto_%s_t' % c_name
                defs += "ctypedef %s\n" % (cy_proto.replace('(*)', proto_name))
                defs += "cdef %s *%s_var\n" % (proto_name, proto_name)
                defs += "%s_var = &_func_%s\n" % (proto_name, c_name)
            else:
                # redeclare the function, so that the assumed
                # signature is checked at compile time
                defs += "cdef extern from \"%s\":\n" % header
                defs += "    pass\n"
                new_name = "_func_%s \"%s\"" % (c_name, c_name)
                defs += "cdef extern %s\n" % (c_proto.replace('(*)', new_name))

    toplevel = "\n".join(all_loops.values() + [defs, toplevel])

    f = open(filename, 'wb')
    f.write("""\
# This file is automatically generated by generate_ufuncs.py.
# Do not edit manually!

cimport numpy as np
cimport libc

np.import_array()
np.import_ufunc()

""")

    f.write(toplevel)

    f.write(extra_code)

    f.close()


def main():
    p = optparse.OptionParser(usage=__doc__.strip())
    options, args = p.parse_args()
    if len(args) != 0:
        p.error('invalid number of arguments')

    generate("_ufuncs.pyx", UFUNCS, EXTRA_CODE)
    generate("_ufuncs_cxx.pyx", UFUNCS_CXX, EXTRA_CODE_CXX)

    subprocess.call(['cython', '_ufuncs.pyx'])
    subprocess.call(['cython', '--cplus', '-o', '_ufuncs_cxx.cxx',
                     '_ufuncs_cxx.pyx'])

    # Strip comments
    for fn in ['_ufuncs.c', '_ufuncs_cxx.cxx']:
        f = open(fn, 'r')
        text = f.read()
        f.close()

        r = re.compile(r'/\*(.*?)\*/', re.S)

        text = r.sub('', text)
        f = open(fn, 'w')
        f.write(text)
        f.close()

if __name__ == "__main__":
    main()
