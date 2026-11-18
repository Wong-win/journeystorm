import { defineCollection, z } from "astro:content";

const articles = defineCollection({
  schema: z.object({
    title: z.string(),
    date: z.string(),
    postSlug: z.string(),
    categories: z.array(z.string()).default([]),
    categorySlugs: z.array(z.string()).default([]),
    excerpt: z.string().optional(),
    image: z.string().optional(),
    urlPath: z.string(),
    /**
     * Position fixe dans le flux de la page d'accueil (1 = premier article).
     * Un article qui porte ce champ est retiré du classement par date puis
     * réinséré à l'emplacement demandé ; le reste du flux continue de défiler
     * normalement. Absent = classement normal par date décroissante.
     */
    homePosition: z.number().optional(),
  }),
});

export const collections = { articles };
