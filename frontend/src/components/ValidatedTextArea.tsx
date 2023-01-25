import React from "react";
import {
  useField,
  FieldAttributes,
} from "formik";

import { 
  TextField 
} from "@mui/material";

const ValidatedTextArea : React.FC<FieldAttributes<object>> = ({
  placeholder,
  type,
  ...props
}) => {
  const [field, meta] = useField<object>(props);

  const errorText = (meta.error && meta.touched) ? meta.error : "";
  return (
    <TextField
      placeholder={placeholder}
      margin="normal"
      label={placeholder}
      {...field}
      helperText={errorText}
      error={!!errorText}
      type={type}
      fullWidth
      multiline
      rows={4}
    />
  );
};

export default ValidatedTextArea;