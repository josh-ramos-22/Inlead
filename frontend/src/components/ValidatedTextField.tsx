import React from 'react';
import {
  Formik,
  Field,
  Form,
  useField,
  FieldAttributes,
  FieldArray
} from "formik";

import { 
  TextField 
} from '@mui/material';

const ValidatedTextField : React.FC<FieldAttributes<{}>> = ({
  placeholder,
  type,
  ...props
}) => {
  const [field, meta] = useField<{}>(props);

  const errorText = (meta.error && meta.touched) ? meta.error : "";
  return (
    <TextField
      placeholder={placeholder}
      margin="normal"
      required
      label={placeholder}
      {...field}
      helperText={errorText}
      error={!!errorText}
      type={type}
      fullWidth
    />
  )
}

export default ValidatedTextField