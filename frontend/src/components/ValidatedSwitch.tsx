import React from "react";

import {
  useField,
  FieldAttributes
} from "formik";

import { 
  FormControlLabel,
  FormHelperText,
  Switch
} from "@mui/material";

type MySwitchProps = { label: string, helperText?: string } & FieldAttributes<object>;

const ValidatedSwitch: React.FC<MySwitchProps> = ({ label, helperText, ...props }) => {
  const [field] = useField<object>(props);

  return ( 
    <>
      <FormControlLabel {...field} control={<Switch />} label={label} />

      {helperText && <FormHelperText>{helperText}</FormHelperText>}
      
    </>
  );
};

export default ValidatedSwitch;