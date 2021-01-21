import numpy as np
import sympy as sp
import warnings
import csv
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sympy.utilities.lambdify import lambdify
import similaritymeasures

a0,a1,a2,a3,a4,a5,x,eps = sp.symbols('a_0 a_1 a_2 a_3 a_4 a_5 x \Epsilon')

unbounded_catalog = [
    {
        "func": (a3 + a0*x),
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
        "func": (a3 + a0*2**(a1*(x/a4))),
        "kind": "exponential",
    },
    {
        "func": (a3 + a0*sp.factorial(a1*(x/a4))),
        "kind": "factorial"
    }
]

common_catalog = [
    {
        "func": (a3 + a0*x),
        "kind": "linear",
    },
    {
        "func": (a3 + a0 * (x/a4)**a1),
        "kind": "polynomial",
        "bounds": {
            a3: [-4000,4000],
            a1: [1.2, 50],
            a4: [0.3,30],
        },
    },
    {
        "func": (a3 + a0*sp.log(x/a4)**a1),
        "kind": "polylogarithmic",
        "bounds": {
            a3: [-4000,4000],
            a1: [-80,80],
            a4: [0.3,30],
        },
    },
    {
        "func": (a3 + a0*(x/a4)*sp.log(x/a4)),
        "kind": "linearithmic",
        "bounds": {
            a3: [-4000,4000],
            a4: [-4,4],
            a0: [-10,10],
        },
    },
    {
        "func": (a3 + a0*(x/a4)*(a1*sp.log(x/a4)**a2)),
        "kind": "quasilinear",
        "bounds": {
            a2: [1,100],
        },
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
        "func": (2**(a1*x)),
        "kind": "exp_2",
        "bounds": {
            a0: [-40000,40000],
            a1: [1,100],
        },
    },
    {
        "func": (a0 + sp.exp(a1*x)),
        "kind": "exp_e",
        "bounds": {
            a0: [1,1000],
        },
    },
    {
        "func": (a3 + a0*sp.factorial(a1*(x/a4))),
        "kind": "factorial",
        "bounds": {
            a0: [-50000,50000],
            a4: [0.5,10000],
        },
    }
]

def prepare_func(catalog_key,catalog):
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

    LB = []
    UB = []
    if "bounds" in func_found:
        for arg_sym in args_ordered:
            if arg_sym == x:
                continue
            if arg_sym in func_found["bounds"]:
                bounds_for_sym = o["bounds"][arg_sym]
                LB.append(bounds_for_sym[0])
                UB.append(bounds_for_sym[1])
            else:
                LB.append(-np.inf)
                UB.append(+np.inf)
    else:
        num = (len(args_ordered)-1)
        LB = (-np.inf,) * num
        UB = (+np.inf,) * num

    return {
        "py_func": lambdify(args_ordered, func_found["func"]),
        "func"   : func_found["func"],
        "args"   : args_ordered,
        "bounds" : tuple([LB,UB]),
    }

def fit_func(cli_args, catalog_key,catalog,X,Y):
    f_to_fit = prepare_func(catalog_key,catalog)

    if cli_args.debug is not None and cli_args.debug == True:
        print(f_to_fit)
    maxfev = 4 * (10**5)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        popt, pcov = curve_fit(f_to_fit["py_func"], X,Y, maxfev=maxfev, bounds=f_to_fit["bounds"])
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

def match_catalog(cli_args,X,Y,catalog):
    plot_data_arr = []

    for elem_catalog in catalog:
        try:
            catalog_label = elem_catalog["kind"]
            f = fit_func(cli_args,catalog_label,catalog,X,Y)
            fitted_py_func = f["fitted_py_func"]
            F_X = fitted_py_func(X)

            # sum_residuals = sum(abs(Y - F_X))
            A=np.zeros((len(X),2))
            B=np.zeros((len(X),2))
            A[:,0]=X
            A[:,1]=Y
            B[:,0]=X
            B[:,1]=F_X
            similarity, dummy = similaritymeasures.dtw(A,B)

            plot_data_arr.append({
                "X": X,
                "F[X]": F_X,
                "F": fitted_py_func,
                "catalog_label": catalog_label,
                "popt": f["popt"],
                "F_str": str(f["func"]),
                "F_sympy_str": str(f["fitted_sympy_func"]),
                "similarity": similarity,
            })
        except ValueError as e:
            continue
        except RuntimeError as e:
            continue

    if len(plot_data_arr)==0:
        return plot_data_arr
    else:
        return sorted(plot_data_arr, key=lambda x: x["similarity"])

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

def run_from_file(cli_args,catalog):
    X,Y = read_columns_csv(cli_args.infile,cli_args.col1,cli_args.col2)

    float_formatter = "{:.2f}".format
    np.set_printoptions(formatter={'float_kind':float_formatter})

    plt.figure(figsize=(10,10))
    plot_data = match_catalog(cli_args,X,Y,catalog)
    plt.plot(X,Y,label="recorded_data")
    max_residuals = compute_max_residuals(X,Y)

    cnt = 1
    for pd in plot_data:
        #if pd["similarity"] > max_residuals: continue
        if pd["F[X]"] is np.nan: continue
        try:
            if cli_args.debug==True:
                print("{0},{1},{2},{3}".format(pd["catalog_label"],pd["similarity"],pd["F_str"],pd["popt"]))

            if cli_args.plot_type == 'normal':
                plt.plot(pd["X"],pd["F[X]"],label=pd["catalog_label"])
            elif cli_args.plot_type == 'loglog':
                plt.loglog(pd["X"],pd["F[X]"],label=pd["catalog_label"])
            else:
                raise "Undefined --plot value [{}]".format(cli_args.plot_type);

        except Exception as e:
            print(e)
            pass
        cnt += 1
        if cli_args.top is not None and cnt > cli_args.top: break

    plt.grid(True, ls="-")
    plt.legend(bbox_to_anchor=(0,0.5), loc='center left')

    if cli_args.outfile is None:
        plt.show()
    else:
        plt.savefig(cli_args.outfile)

# __all__ = ['run_from_file','compute_max_residuals','match_catalog','prepare_func','fit_func','default_catalog']
