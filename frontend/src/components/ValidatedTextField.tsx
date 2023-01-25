import React from "react";
import {
  useField,
  FieldAttributes,
} from "formik";

import { 
  TextField 
} from "@mui/material";

type TextFieldProps = { fullWidth?: boolean } & FieldAttributes<object>;

const ValidatedTextField : React.FC<TextFieldProps> = ({
  placeholder,
  type,
  fullWidth=false,
  ...props
}) => {
  const [field, meta] = useField<object>(props);

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
      fullWidth={fullWidth}
    />
  );
};

export default ValidatedTextField;