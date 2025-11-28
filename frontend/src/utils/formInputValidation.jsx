/* */

import * as yup from "yup";


export const brandValidationSchema = yup.object(
  {
    name: yup.string()
      .required("Brand name is required")
      .min(3, "Minimum of 3 characters.")
      .max(200, "Maximum of 200 characters."),
    is_active: yup.boolean()
  }
);

export const categoryValidationSchema = yup.object(
  {
    name: yup.string()
      .required("Category name is required.")
      .min(3, "Minimum of 3 characters.")
      .max(200, "Maximum of 200 characters."),
    description: yup.string()
      .max(2000, "Maximum of 2000 characters."),
  }
);

export const employeeRegistrationValidationSchema = yup.object(
  {
    username: yup.string()
    .required("Username is required")
    .min(3, "Minimum of 3 characters")
    .max(200, "Maximum of 200 characters"),
    email: yup.string()
      .email("Invalid email format")
      .required("Email is required"),
    password: yup.string()
      .required("Password is required")
      .min(8, "Password must be at least 8 characters")
      .max(200, "Maximum of 200 characters")
      .matches(/[0-9]/, "Password must contain at least one number")
      .matches(/[A-Z]/, "Password must contain at least one uppercase")
      .matches(/[a-z]/, "Password must contain at least one lowercase"),
    confirm_password: yup.string()
        .required("Confirm password is required")
        .oneOf([yup.ref("password")], "Password must match"),
    first_name: yup.string()
      .required("First name is required")
      .min(3, "Minimum of 3 characters")
      .max(200, "Maximum of 200 characters"),
    middle_name: yup.string(),
    last_name: yup.string()
      .required("Last name is required")
      .min(3, "Minimum of 3 characters")
      .max(200, "Maximum of 200 characters"),
    home_address: yup.string()
      .required("Home address is required")
      .min(10, "Minimum of 10 characters")
      .max(500, "Maximum of 500 characters"),
    role: yup.string()
      .required("Employee role is required")
      .oneOf(["manager", "salesperson"], "Role must be either manager or salesperson"),
    is_admin: yup.boolean()
  }
)

export const employeeLoginValidationSchema = yup.object(
  {
    email_or_username: yup.string()
    .required("Email or username is required")
    .min(3, "Minimum of 3 characters")
    .max(200, "Maximum of 200 characters"),
    password: yup.string().required("Password is required")
  }
)

export const profileUpdateValidationSchema = yup.object(
  {
    first_name: yup.string()
      .required("First name is required")
      .min(3, "Minimum of 3 characters")
      .max(200, "Maximum of 200 characters"),
    middle_name: yup.string(),
    last_name: yup.string()
      .required("Last name is required")
      .min(3, "Minimum of 3 characters")
      .max(200, "Maximum of 200 characters"),
    home_address: yup.string()
      .required("Home address is required")
      .min(10, "Minimum of 10 characters")
      .max(500, "Maximum of 500 characters"),
  }
)

export const productValidationSchema = yup.object(
  {
    barcode: yup.string().max(20, "Maximum of 20 characters."),
    name: yup.string()
      .required("Product name is required.")
      .min(3, "Minimum of 3 characters.")
      .max(200, "Maximum of 200 characters."),
    unit_cost_price: yup.number()
      .transform((value, originalValue) => (originalValue === '' ? undefined : value))
      .moreThan(0, "Unit cost price must be greater than zero.")
      .required("Unit cost price is required."),
    unit_selling_price: yup.number()
      .transform((value, originalValue) => (originalValue === '' ? undefined : value))
      .moreThan(0, "Unit selling price must be greater than zero.")
      .required("Unit selling price is required."),
    category_id: yup.string()
      .required()
      .length(36, "Must be exactly 36 characters long."),
    brand_id: yup.string()
      .transform((value, originalValue) => (originalValue === "" ? null : value))
      .nullable(),
    brand_name: yup.string()
      .transform((value, originalValue) => (originalValue === "" ? null : value))
      .max(200)
      .nullable(),
    created_at: yup.date()
      .transform((value, originalValue) => (originalValue === "" ? null : value))
      .nullable(),
    last_updated: yup.date()
      .transform((value, originalValue) => (originalValue === "" ? null : value))
      .nullable(),

  }
).test(
  'brand-validation',
  'Brand name is required.',
  (obj) => {
    // obj is the entire object with all fields
    return (obj.brand_id?.trim() || obj.brand_name?.trim());
  }
)


