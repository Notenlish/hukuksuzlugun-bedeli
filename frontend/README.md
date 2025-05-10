# next-js-boilerplate
 Repo for easily setting up Auth.js + Prisma + Shadcn UI using Next.js
 Will use Postgre SQL.
 Has contact support with discord webhooks.

 It does not have email or phone verification. If you want those, a more comprehensive template can be found here: https://github.com/nextauthjs/next-auth-example/ 


# Setting Up:
create a .env file in `my-app/.env`
set DATABASE_URL in .env file

for AUTH_SECRET, you can generate it like so: `npx auth secret`

you can change the auth providers in `auth.config.ts`.
Currently there are Credentials Provider and Github. You need to setup `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` if you want to use github.

For DB related stuff, you can just create a NEON database from vercel and copy paste the environment variables to `.env`

also set up `CONTACT_WEBHOOK` for discord webhook.
Also set up `NEXTAUTH_URL`. 

if prisma says it coudlnt find DATABASE_URL yet youve specified it in .env.local, you need to create .env file and put DATABASE_URL there as well.



# Commands

`npx prisma generate`
`npx prisma db push`
