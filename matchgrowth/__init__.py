import numpy as np
import sympy as sp
import warnings
import csv
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sympy.utilities.lambdify import lambdify

a0,a1,a2,a3,a4,a5,x,eps = sp.symbols('a_0 a_1 a_2 a_3 a_4 a_5 x \Epsilon')

default_catalog = [
    {
        "func": (a3 + a0*x+a1),
        "kind": "linear",
    },
    {
        "func": (a3 + a0 * (x/a4)**a1),
        "kind": "polynomial",
    },
    {
        "func": (a3 + a0*sp.log(x/a4)**a1),
        "kind": "polylogarithmic",
    },
    {
        "func": (a3 + a0*(x/a4)*sp.log(x/a4)),
        "kind": "linearithmic",
    },
    {
        "func": (a3 + a0*(x/a4)*(a1*sp.log(x/a4)**a2)),
        "kind": "quasilinear",
    },
    {
        "func": (a3 + a0*sp.log(x/a4)),
        "kind": "logarithmic",
    },
    {
        "func": (a3 + a0*(x/a4)**(a1*sp.log(x/a4)) ),
        "kind": "quasipolynomial",
    },
    {
        "func": (a3 + a0*2**(a1*(x/a4)**eps)),
        "kind": "subexponential",
    },
    {
        "func": (a3 + a0*2**(a1*(x/a4))),
        "kind": "exponential",
    },
    {
        "func": (a3 + a0*sp.factorial(a1*(x/a4))),
        "kind": "factorial"
    }
]

def prepare_func(catalog_key,catalog=default_catalog):
    func_found = None
    for o in catalog:
        if o["kind"] == catalog_key:
            func_found = o
            break

    if func_found is None:
        return None
    
    args_ordered = list(func_found["func"].free_symbols)
    args_ordered.remove(x)
    args_ordered.insert(0,x)

    return {
        "py_func": lambdify(args_ordered, func_found["func"]),
        "func"   : func_found["func"],
        "args"   : args_ordered,
    }

def fit_func(catalog_key,catalog,X,Y):
    f_to_fit = prepare_func(catalog_key)
    maxfev = 4 * (10**4)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        popt, pcov = curve_fit(f_to_fit["py_func"], X,Y, maxfev=maxfev)
    args_ = f_to_fit["args"]
    args_.pop(0)
    subs_arg = dict(list(zip(args_,popt)))
    fitted_sympy_func = f_to_fit["func"].subs(subs_arg)
    fitted_py_func = lambdify([x], fitted_sympy_func)
    return {
        "func"             : f_to_fit["func"],
        "fitted_sympy_func": fitted_sympy_func,
        "fitted_py_func"   : fitted_py_func,
        "popt"             : subs_arg,
    }

def match_catalog(X,Y,catalog=default_catalog):
    plot_data_arr = []

    for elem_catalog in catalog:
        try:
            catalog_label = elem_catalog["kind"]
            f = fit_func(catalog_label,catalog,X,Y)
            fitted_func = f["fitted_py_func"]
            sum_residuals = sum(abs(Y - fitted_func(X)))
            plot_data_arr.append({
                "X": X,
                "F[X]": fitted_func(X),
                "F": fitted_func,
                "catalog_label": catalog_label,
                "popt": f["popt"],
                "F_str": str(f["func"]),
                "sum_residuals": sum_residuals,
            })
        except RuntimeError as e:
            continue

    if len(plot_data_arr)==0:
        return plot_data_arr
    else:
        return sorted(plot_data_arr, key=lambda x: x["sum_residuals"])

def read_columns_csv(filepath,col1,col2):
    with open(filepath,'r') as f:
        has_header = csv.Sniffer().has_header(f.read(1024))
        f.seek(0)

        data_iter = csv.DictReader(f,delimiter = ",",quotechar = '"')
        data = [data for data in data_iter]
        X = np.asarray(list(map(lambda x: x[col1] ,data)), dtype=np.float64)
        Y = np.asarray(list(map(lambda x: x[col2] ,data)), dtype=np.float64)

        if has_header:
            np.delete(X,0)
            np.delete(Y,0)

        return X,Y

def compute_max_residuals(X,Y):
    total_data_area = abs(max(X)-min(X)) * abs(max(Y)-min(Y))
    max_percent = 0.02
    return total_data_area * max_percent

def run_from_file(infile,col1,col2,catalog=default_catalog,outfile=None,top=None):
    X,Y = read_columns_csv(infile,col1,col2)

    float_formatter = "{:.2f}".format
    np.set_printoptions(formatter={'float_kind':float_formatter})

    plt.figure(figsize=(10,10))
    plot_data = match_catalog(X,Y,catalog)
    plt.plot(X,Y,label="recorded_data")
    max_residuals = compute_max_residuals(X,Y)

    cnt = 1
    for pd in plot_data:
        if pd["sum_residuals"] > max_residuals: continue
        if pd["F[X]"] is np.nan: continue
        plt.plot(pd["X"],pd["F[X]"],label=pd["catalog_label"])
        print(pd["catalog_label"],pd["sum_residuals"],pd["popt"])
        cnt += 1
        if top is not None and cnt > top: break

    plt.grid(True, ls="-")
    plt.legend(bbox_to_anchor=(0,0), loc='upper left', borderaxespad=0.)

    if outfile is None:
        plt.show()
    else:
        plt.savefig(outfile)


