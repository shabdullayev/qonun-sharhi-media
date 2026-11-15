const vercelUrl = process.env.VERCEL_PROJECT_PRODUCTION_URL;

/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  poweredByHeader: false,
  env: {
    // Sayt manzili: qo‘lda berilmagan bo‘lsa, Vercel’dagi asosiy domen olinadi.
    NEXT_PUBLIC_SITE_URL: process.env.NEXT_PUBLIC_SITE_URL || (vercelUrl ? `https://${vercelUrl}` : ""),
  },
};
export default nextConfig;
