// Generado automaticamente por scraper/generar_modelo.py
// Modelo de riesgo de desercion — datos reales UNAL Sede Bogota (2025-2)
//
// Metodo: modelo multiplicativo de riesgo (log-lineal / Naive Bayes multinomial).
// Para cada variable X con categorias c_i:
//   coeficiente[c_i] = log( tasa_observada(c_i) / tasa_base )
// Prediccion final:
//   log_odds = logit(tasa_base) + sum(coef_Xi)
//   riesgo   = sigmoid(log_odds)
//
// Interpretacion: cada coeficiente representa cuanto aumenta o disminuye
// el log-odds de desercion respecto al promedio global (tasa_base = 0.0507).
// Coef > 0 => mayor riesgo; Coef < 0 => menor riesgo.

export const TASA_BASE = 0.05074506645187274;

// Coeficientes por variable (log risk ratio respecto a tasa_base)
export const COEFS = {
  programa: {
    "Administración de Empresas": 0.19917310,
    "Antropología": -0.07036125,
    "Arquitectura": -0.59923916,
    "Artes Plásticas": -0.15937262,
    "Biología": -0.64506533,
    "Ciencia Política": 0.18678410,
    "Ciencias de La Computación": 0.37242027,
    "Cine y Televisión": 0.08764941,
    "Contaduria Pública": 0.27479726,
    "Derecho": -0.00889167,
    "Diseño Gráfico": -1.15688880,
    "Diseño Industrial": -0.55274569,
    "Economía": -0.02054405,
    "Enfermería": 0.20559860,
    "Español y Filología Clásica": 0.62780351,
    "Estadística": 0.32857958,
    "Estudios Literarios": -0.19189101,
    "Farmacia": -0.49187219,
    "Filología E Idiomas": 0.13071619,
    "Filosofía": 0.48224091,
    "Fisioterapia": 0.33219042,
    "Fonoaudiología": -0.45304633,
    "Física": -0.00889167,
    "Geografía": 0.55545765,
    "Geología": -0.23543182,
    "Historia": -0.26555011,
    "Ingeniería Agronómica": 0.46094291,
    "Ingeniería Agrícola": 0.78225538,
    "Ingeniería Civil": -0.08201186,
    "Ingeniería Electrónica": -0.30386139,
    "Ingeniería Eléctrica": 0.24085132,
    "Ingeniería Industrial": -0.10659894,
    "Ingeniería Mecatrónica": -0.55916557,
    "Ingeniería Mecánica": 0.12447067,
    "Ingeniería Química": -0.00428867,
    "Ingeniería de Sistemas y Computación": -0.13144385,
    "Lingüística": 0.22637066,
    "Matemáticas": 0.60271837,
    "Medicina": -0.59630845,
    "Medicina Veterinaria": -0.02721391,
    "Música Instrumental": -0.35482870,
    "Nutrición y Dietética": -0.78025924,
    "Odontología": -0.15875208,
    "Psicología": 0.09215768,
    "Química": 0.27289068,
    "Sociología": 0.19913550,
    "Terapia Ocupacional": -0.03726425,
    "Trabajo Social": -0.04045914,
    "Zootecnia": 0.19592964,
  },

  estrato: {
    "1": 0.06652950,
    "2": -0.11601292,
    "3": 0.05469591,
    "4": 0.10926125,
    "5": 0.08473820,
    "6": -0.31489599,
  },

  tipo_colegio: {
    "Oficial": -0.21638026,
    "Otro": -0.25118017,
    "Privado": -0.29984396,
  },

  genero: {
    "Femenino": -0.16886136,
    "Masculino": 0.14263469,
    "No Binario": 0.34188355,
  },

  nivelacion_matematicas: {
    "NO": 0.01808666,
    "SI": 0.28192008,
  },

  nivelacion_lectoescritura: {
    "NO": 0.02826014,
    "SI": 0.18072022,
  },
} satisfies Record<string, Record<string, number>>;

// Opciones validas para cada campo (para los <select> en la UI)
export const OPCIONES = {
  programa: [
  "Administración de Empresas",
  "Antropología",
  "Arquitectura",
  "Artes Plásticas",
  "Biología",
  "Ciencia Política",
  "Ciencias de La Computación",
  "Cine y Televisión",
  "Contaduria Pública",
  "Derecho",
  "Diseño Gráfico",
  "Diseño Industrial",
  "Economía",
  "Enfermería",
  "Español y Filología Clásica",
  "Estadística",
  "Estudios Literarios",
  "Farmacia",
  "Filología E Idiomas",
  "Filosofía",
  "Fisioterapia",
  "Fonoaudiología",
  "Física",
  "Geografía",
  "Geología",
  "Historia",
  "Ingeniería Agronómica",
  "Ingeniería Agrícola",
  "Ingeniería Civil",
  "Ingeniería Electrónica",
  "Ingeniería Eléctrica",
  "Ingeniería Industrial",
  "Ingeniería Mecatrónica",
  "Ingeniería Mecánica",
  "Ingeniería Química",
  "Ingeniería de Sistemas y Computación",
  "Lingüística",
  "Matemáticas",
  "Medicina",
  "Medicina Veterinaria",
  "Música Instrumental",
  "Nutrición y Dietética",
  "Odontología",
  "Psicología",
  "Química",
  "Sociología",
  "Terapia Ocupacional",
  "Trabajo Social",
  "Zootecnia"
],
  estrato: ["1", "2", "3", "4", "5", "6"],
  tipo_colegio: ["Oficial", "Otro", "Privado"],
  genero: ["Masculino", "Femenino", "No Binario"],
  nivelacion_matematicas: ["NO", "SI"],
  nivelacion_lectoescritura: ["NO", "SI"],
} as const;

export type PerfilEstudiante = {
  programa: string;
  estrato: string;
  tipo_colegio: string;
  genero: string;
  nivelacion_matematicas: "NO" | "SI";
  nivelacion_lectoescritura: "NO" | "SI";
};

function logit(p: number): number {
  return Math.log(p / (1 - p));
}

function sigmoid(x: number): number {
  return 1 / (1 + Math.exp(-x));
}

/**
 * Estima la probabilidad de desercion para un perfil de estudiante.
 * Devuelve un numero en [0, 1].
 *
 * Si una variable no esta en la tabla de coeficientes, se ignora
 * (equivale a asumir riesgo promedio para esa dimension).
 */
export function predecir(perfil: PerfilEstudiante): number {
  let logOdds = logit(TASA_BASE);

  const vars: [keyof typeof COEFS, string][] = [
    ["programa",                perfil.programa],
    ["estrato",                 perfil.estrato],
    ["tipo_colegio",            perfil.tipo_colegio],
    ["genero",                  perfil.genero],
    ["nivelacion_matematicas",  perfil.nivelacion_matematicas],
    ["nivelacion_lectoescritura", perfil.nivelacion_lectoescritura],
  ];

  for (const [dim, valor] of vars) {
    const coef = (COEFS[dim] as Record<string, number>)[valor];
    if (coef !== undefined) logOdds += coef;
  }

  return sigmoid(logOdds);
}

// Peor perfil alcanzable con los datos reales del dashboard.
// Sirve como referencia para escalar la barra de riesgo.
export const RIESGO_MAX = predecir({
  programa:                  "Ingeniería Agrícola", // tasa más alta (11.1 %)
  estrato:                   "4",                   // estrato con mayor tasa
  tipo_colegio:              "Oficial",             // menor reducción de riesgo
  genero:                    "Masculino",           // tasa más alta con muestra grande
  nivelacion_matematicas:    "SI",
  nivelacion_lectoescritura: "SI",
});
