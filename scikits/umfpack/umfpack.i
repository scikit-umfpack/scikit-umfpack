/* -*- C -*- */
#ifdef SWIGPYTHON

%module _umfpack

/*
  See umfpack.py for more information.

  Created by: Robert Cimrman
*/

%{
#include <umfpack.h>
#include "numpy/arrayobject.h"
%}


%feature("autodoc", "1");

#include <umfpack.h>

typedef int64_t UF_long;

/* Convert 32-bit integer from Python --> C */
%typemap(in) int32_t {
  $1 = (int32_t)PyLong_AsLong($input);
}

/* Convert from C --> Python */
%typemap(out) int32_t {
  $result = PyLong_FromLong($1);
}

/* Convert 64-bit integer from Python --> C */
%typemap(in) int64_t {
  $1 = (int64_t)PyLong_AsLongLong($input);
}

/* Convert 64-bit integer from C --> Python */
%typemap(out) int64_t {
  $result = PyLong_FromLongLong($1);
}

%init %{
    import_array();
%}

%{
/*!
  Appends @a what to @a where. On input, @a where need not to be a tuple, but on
  return it always is.

  @par Revision history:
  - 17.02.2005, c
*/
PyObject *helper_appendToTuple( PyObject *where, PyObject *what ) {
  PyObject *o2, *o3;

  if ((!where) || (where == Py_None)) {
    where = what;
  } else {
    if (!PyTuple_Check( where )) {
      o2 = where;
      where = PyTuple_New( 1 );
      PyTuple_SetItem( where, 0, o2 );
    }
    o3 = PyTuple_New( 1 );
    PyTuple_SetItem( o3, 0, what );
    o2 = where;
    where = PySequence_Concat( o2, o3 );
    Py_DECREF( o2 );
    Py_DECREF( o3 );
  }
  return where;
}

/*!
  Gets PyArrayObject from a PyObject.

  @par Revision history:
  - 22.02.2005, c
  - 03.03.2005
  - 25.11.2005
  - 30.11.2005
  - 01.12.2005
*/
PyArrayObject *helper_getCArrayObject( PyObject *input, int type,
				       int minDim, int maxDim ) {
  PyArrayObject *obj;

  if (PyArray_Check( input )) {
    obj = (PyArrayObject *) input;
    if (!PyArray_ISCARRAY( obj )) {
      PyErr_SetString( PyExc_TypeError, "not a C array" );
      return NULL;
    }
    obj = (PyArrayObject *)
      PyArray_ContiguousFromAny( input, type, minDim, maxDim );
    if (!obj) return NULL;
  } else {
    PyErr_SetString( PyExc_TypeError, "not an array" );
    return NULL;
  }
  return obj;
}
%}

/*!
  Use for arrays as input arguments. Could be also used for changing an array
  in place.

  @a rtype ... return this C data type
  @a ctype ... C data type of the C function
  @a atype ... PyArray_* suffix

  @par Revision history:
  - 30.11.2005, c
*/
#define ARRAY_IN( rtype, ctype, atype ) \
%typemap( in ) (ctype *array) { \
  PyArrayObject *obj; \
  obj = helper_getCArrayObject( $input, NPY_##atype, 1, 1 ); \
  if (!obj) return NULL; \
  $1 = (rtype *) obj->data; \
  Py_DECREF( obj ); \
};

/*!
  @par Revision history:
  - 30.11.2005, c
*/
#define CONF_IN( arSize ) \
%typemap( in ) (double conf [arSize]) { \
  PyArrayObject *obj; \
  obj = helper_getCArrayObject( $input, NPY_DOUBLE, 1, 1 ); \
  if (!obj) return NULL; \
  if ((obj->nd != 1) || (obj->dimensions[0] != arSize)) { \
    PyErr_SetString( PyExc_ValueError, "wrong Control/Info array size" ); \
    Py_DECREF( obj ); \
    return NULL; \
  } \
  $1 = (double *) obj->data; \
  Py_DECREF( obj ); \
};

/*!
  @par Revision history:
  - 01.12.2005, c
  - 02.12.2005
*/
#define OPAQUE_ARGOUT( ttype ) \
%typemap( in, numinputs=0 ) ttype* opaque_argout( ttype tmp ) { \
  $1 = &tmp; \
}; \
%typemap( argout ) ttype* opaque_argout { \
  PyObject *obj; \
  obj = SWIG_NewPointerObj( (ttype) (*$1), $*1_descriptor, 0 ); \
  $result = helper_appendToTuple( $result, obj ); \
};

/*!
  @par Revision history:
  - 02.12.2005, c
*/
#define OPAQUE_ARGINOUT( ttype ) \
%typemap( in ) ttype* opaque_arginout( ttype tmp ) { \
  if ((SWIG_ConvertPtr( $input,(void **) &tmp, $*1_descriptor, \
			SWIG_POINTER_EXCEPTION)) == -1) return NULL; \
  $1 = &tmp; \
}; \
%typemap( argout ) ttype* opaque_arginout { \
  PyObject *obj; \
  obj = SWIG_NewPointerObj( (ttype) (*$1), $*1_descriptor, 0 ); \
  $result = helper_appendToTuple( $result, obj ); \
};

ARRAY_IN( int32_t, const int32_t, INT32 )
%apply const int32_t *array {
    const int32_t Ap [ ],
    const int32_t Ai [ ]
};

ARRAY_IN( int64_t, const int64_t, INT64 )
%apply const int64_t *array {
    const int64_t Ap [ ],
    const int64_t Ai [ ]
};

ARRAY_IN( double, const double, DOUBLE )
%apply const double *array {
    const double Ax [ ],
    const double Az [ ],
    const double B [ ],
    const double Bx [ ],
    const double Bz [ ]
};

ARRAY_IN( double, double, DOUBLE )
%apply double *array {
    double X [ ],
    double Xx [ ],
    double Xz [ ]
};

CONF_IN( UMFPACK_CONTROL )
%apply (double conf [UMFPACK_CONTROL]) {
    double Control [ANY]
};

CONF_IN( UMFPACK_INFO )
%apply double conf [UMFPACK_INFO] {
    double Info [ANY]
};

OPAQUE_ARGOUT( void * )
%apply  void ** opaque_argout {
    void **Symbolic,
    void **Numeric
}

// OPAQUE_ARGINOUT( void * )
// %apply  void ** opaque_arginout {
//     void **Symbolic,
//     void **Numeric
// }

/*
 * wnbell - attempt to get L,U,P,Q out
 */
%include "typemaps.i"
%apply int *OUTPUT {
    int32_t *lnz,
    int32_t *unz,
    int32_t *n_row,
    int32_t *n_col,
    int32_t *nz_udiag
};
%apply int *OUTPUT {
    int64_t *lnz,
    int64_t *unz,
    int64_t *n_row,
    int64_t *n_col,
    int64_t *nz_udiag
};

ARRAY_IN( double, double, DOUBLE )
%apply double *array {
    double Lx [ ],
    double Lz [ ],
    double Ux [ ],
    double Uz [ ],
    double Dx [ ],
    double Dz [ ],
    double Rs [ ]
};

ARRAY_IN( int32_t, int32_t, INT32 )
%apply int32_t *array {
    int32_t Lp [ ],
    int32_t Lj [ ],
    int32_t Up [ ],
    int32_t Ui [ ],
    int32_t P [ ],
    int32_t Q [ ]
};
%apply int *OUTPUT { int32_t *do_recip};

ARRAY_IN( int64_t, int64_t, INT64 )
%apply int64_t *array {
    int64_t Lp [ ],
    int64_t Lj [ ],
    int64_t Up [ ],
    int64_t Ui [ ],
    int64_t P [ ],
    int64_t Q [ ]
};
%apply int *OUTPUT { int64_t *do_recip};

%include <umfpack.h>

#endif // SWIGPYTHON
