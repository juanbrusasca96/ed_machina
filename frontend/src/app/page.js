"use client";
import { Controller, useForm } from 'react-hook-form';
import * as yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import { Button, FormControl, FormHelperText, Grid2, InputLabel, MenuItem, Select, Snackbar, TextField } from '@mui/material';
import { useEffect, useState } from 'react';
import axiosInstance from '@/axiosConfig';

export default function Home() {
  const [emailExists, setEmailExists] = useState(true);
  const [careers, setCareers] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [open, setOpen] = useState(false);
  const [id, setId] = useState(0);

  useEffect(() => {
    const getData = async () => {
      try {
        const response = await axiosInstance.get('/front/career/get_all');
        setCareers(response.data);
      }
      catch (error) {
        console.error(error);
      }
    }
    getData();
  }, []);

  const schema = yup.object().shape({
    person_name: yup.string()
      .max(50, 'Nombre no puede tener más de 50 caracteres')
      .when([], {
        is: () => !emailExists,
        then: (schema) => schema
          .required('Nombre es requerido')
          .min(3, 'Nombre debe tener al menos 3 caracteres')
          .matches(/^[A-Za-z]+$/, 'Nombre solo debe contener letras')
      }),
    person_last_name: yup.string()
      .max(50, 'Apellido no puede tener más de 50 caracteres')
      .when([], {
        is: () => !emailExists,
        then: (schema) => schema
          .required('Apellido es requerido')
          .min(3, 'Apellido debe tener al menos 3 caracteres')
          .matches(/^[A-Za-z]+$/, 'Apellido solo debe contener letras')
      }),
    person_email: yup
      .string()
      .email('Email debe ser un correo válido')
      .matches(
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
        'Email debe ser un correo válido'
      )
      .required('Email es requerido'),
    person_address: yup.string()
      .max(100, 'Dirección no puede tener más de 100 caracteres')
      .when([], {
        is: () => !emailExists,
        then: (schema) => schema
          .required('Dirección es requerida')
          .min(5, 'Dirección debe tener al menos 5 caracteres')
      }),
    person_phone: yup.string()
      .when([], {
        is: () => !emailExists,
        then: (schema) => schema
          .required('Número de teléfono es requerido')
          .matches(
            /^\+?\d{7,15}$/,
            'Número de teléfono debe tener entre 7 y 15 dígitos')
          .test(
            'phone-format',
            'Número de teléfono debe tener un formato válido (+123456789)',
            (value) => {
              if (!value) return true;
              if (value.length > 10 && !value.startsWith('+')) {
                return false;
              }
              return true;
            }
          ),
      }),
    career_id: yup.number().required('Carrera es requerida'),
    enrollment_year: yup.string().required('Año de inscripción es requerido'),
    subject_id: yup.number().required('Materia es requerida'),
    study_time: yup.string().required('Tiempo de estudio es requerido'),
    subject_attempts: yup.string().required('Intentos de materia es requerido'),
  });

  const defaultValues = {
    person_name: '',
    person_last_name: '',
    person_email: '',
    person_address: '',
    person_phone: '',
    career_id: null,
    enrollment_year: '',
    subject_id: null,
    study_time: '',
    subject_attempts: '',
  };

  const methods = useForm({
    resolver: yupResolver(schema),
    defaultValues,
    mode: 'onBlur',
  });

  const control = methods.control;
  const errors = methods.formState.errors;

  const handleValidateEmail = async (email) => {
    try {
      const response = await axiosInstance.get('/front/person/check_email_exists', {
        params: {
          email,
        },
      });
      setEmailExists(response.data);
      if (response.data) {
        setOpen(true);
      }
    }
    catch (error) {
      console.error(error);
    }
  }

  const handleCareerChange = async (careerId) => {
    try {
      const response = await axiosInstance.get('/front/subject/get_by_career/' + careerId);
      setSubjects(response.data);
    }
    catch (error) {
      console.error(error);
    }
  }

  const cleanObject = (obj) => {
    for (const key in obj) {
      if (obj[key] === '') {
        delete obj[key];
      }
    }
    return obj;
  }

  const onSubmit = async (data) => {
    data.subject = {
      subject_id: data.subject_id,
      study_time: data.study_time,
      subject_attempts: data.subject_attempts,
    }
    data.career = {
      career_id: data.career_id,
      enrollment_year: data.enrollment_year,
    }
    data = cleanObject(data);
    try {
      const response = await axiosInstance.post('/front/person/register', data);
      setId(response.data.person.person_id);
      methods.reset(defaultValues);
    }
    catch (error) {
      console.error(error);
    }
  }

  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }

    setOpen(false);
    setId(0);
  };

  return (
    <Grid2 container justifyContent='center' alignItems='center'>
      <Snackbar
        open={open}
        autoHideDuration={6000}
        onClose={handleClose}
        message="Email ya registrado, puede continuar con la carga de datos"
        severity='success'
      />
      <Snackbar
        open={id !== 0}
        autoHideDuration={10000}
        onClose={handleClose}
        message={`Persona registrada con éxito, ID: ${id}`}
        severity='success'
      />
      <form onSubmit={methods.handleSubmit(onSubmit)} style={{ width: '40%' }}>
        <Grid2 container direction='column' gap={2} width='100%'>
          <Grid2 container direction='row' justifyContent='center' alignItems='center' gap={2} width='100%'>
            <FormControl>
              <Controller
                name='person_email'
                control={control}
                render={({ field, fieldState }) => (
                  <TextField
                    {...field}
                    label='Email'
                    onChange={field.onChange}
                    error={fieldState.invalid}
                    helperText={fieldState.error?.message}
                  />
                )}
              />
            </FormControl>
            <Button
              variant='contained'
              onClick={() => handleValidateEmail(methods.getValues('person_email'))}
            >
              Validar email
            </Button>
          </Grid2>
          {!emailExists &&
            <>
              <FormControl>
                <Controller
                  name='person_name'
                  control={control}
                  render={({ field, fieldState }) => (
                    <TextField
                      {...field}
                      label='Nombre'
                      onChange={field.onChange}
                      error={fieldState.invalid}
                      helperText={fieldState.error?.message}
                    />
                  )}
                />
              </FormControl>
              <FormControl>
                <Controller
                  name='person_last_name'
                  control={control}
                  render={({ field, fieldState }) => (
                    <TextField
                      {...field}
                      label='Apellido'
                      onChange={field.onChange}
                      error={fieldState.invalid}
                      helperText={fieldState.error?.message}
                    />
                  )}
                />
              </FormControl>
              <FormControl>
                <Controller
                  name='person_address'
                  control={control}
                  render={({ field, fieldState }) => (
                    <TextField
                      {...field}
                      label='Dirección'
                      onChange={field.onChange}
                      error={fieldState.invalid}
                      helperText={fieldState.error?.message}
                    />
                  )}
                />
              </FormControl>
              <FormControl>
                <Controller
                  name='person_phone'
                  control={control}
                  render={({ field, fieldState }) => (
                    <TextField
                      {...field}
                      label='Teléfono'
                      onChange={field.onChange}
                      error={fieldState.invalid}
                      helperText={fieldState.error?.message}
                    />
                  )}
                />
              </FormControl>
            </>
          }
          <FormControl>
            <InputLabel id="demo-simple-select-label">Carrera</InputLabel>
            <Controller
              name='career_id'
              control={control}
              rules={{ required: true }}
              render={({ field, fieldState }) => (
                <Select
                  labelId="demo-simple-select-label"
                  id="demo-simple-select"
                  {...field}
                  label='Carrera'
                  onChange={(event) => {
                    field.onChange(event);
                    handleCareerChange(event.target.value);
                  }}
                  value={field.value}
                  error={fieldState.invalid}
                  helperText={fieldState.error?.message}
                >
                  {careers.map((career) => (
                    <MenuItem key={career.career_id} value={career.career_id}>
                      {career.career_name}
                    </MenuItem>
                  ))}
                </Select>
              )}
            />
            <FormHelperText sx={{ color: 'error.main' }}>{errors.career_id?.message}</FormHelperText>
          </FormControl>
          <FormControl>
            <Controller
              name='enrollment_year'
              control={control}
              render={({ field, fieldState }) => (
                <TextField
                  {...field}
                  label='Año de inscripción'
                  onChange={field.onChange}
                  error={fieldState.invalid}
                  helperText={fieldState.error?.message}
                />
              )}
            />
          </FormControl>
          {subjects.length > 0 && <>
            <FormControl>
              <InputLabel id="demo-simple-select-label">Materia</InputLabel>
              <Controller
                name='subject_id'
                control={control}
                rules={{ required: true }}
                render={({ field, fieldState }) => (
                  <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    {...field}
                    label='Materia'
                    onChange={field.onChange}
                    value={field.value}
                    error={fieldState.invalid}
                    helperText={fieldState.error?.message}
                  >
                    {subjects.map((subject) => (
                      <MenuItem key={subject.subject_id} value={subject.subject_id}>
                        {subject.subject_name}
                      </MenuItem>
                    ))}
                  </Select>
                )}
              />
              <FormHelperText sx={{ color: 'error.main' }}>{errors.subject_id?.message}</FormHelperText>
            </FormControl>
            <Grid2 container direction='row' justifyContent='center' alignItems='center' gap={2}>
              <FormControl>
                <Controller
                  name='study_time'
                  control={control}
                  render={({ field, fieldState }) => (
                    <TextField
                      {...field}
                      label='Tiempo de estudio'
                      onChange={field.onChange}
                      error={fieldState.invalid}
                      helperText={fieldState.error?.message}
                    />
                  )}
                />
              </FormControl>
              <FormControl>
                <Controller
                  name='subject_attempts'
                  control={control}
                  render={({ field, fieldState }) => (
                    <TextField
                      {...field}
                      label='Intentos de materia'
                      onChange={field.onChange}
                      error={fieldState.invalid}
                      helperText={fieldState.error?.message}
                    />
                  )}
                />
              </FormControl>
            </Grid2>
          </>}
          <Button type='submit' variant='contained'>Enviar</Button>
        </Grid2>
      </form>
    </Grid2>
  );
}
