export default function Home() {
  return (
    <main className="min-h-screen bg-white">
      <section className="mx-auto flex min-h-screen max-w-5xl flex-col items-center justify-center px-6 py-16 text-center">
        <p className="mb-4 text-sm font-medium uppercase tracking-wider text-gray-500">
          RentFlow
        </p>

        <h1 className="max-w-3xl text-4xl font-semibold tracking-tight text-gray-900 sm:text-5xl">
          La gestion locative, simplement.
        </h1>

        <p className="mt-6 max-w-2xl text-lg leading-8 text-gray-600">
          Gérez vos biens, vos locataires, vos contrats et vos paiements
          depuis un seul endroit.
        </p>

        <div className="mt-8">
          <a
            href="/login"
            className="inline-flex items-center rounded-lg bg-gray-900 px-6 py-3 text-sm font-medium text-white transition hover:bg-gray-800"
          >
            Commencer
          </a>
        </div>

        <div className="mt-16 grid w-full max-w-3xl gap-4 sm:grid-cols-3">
          <div className="rounded-xl border border-gray-200 p-6">
            <h2 className="font-medium text-gray-900">Biens</h2>
            <p className="mt-2 text-sm text-gray-600">
              Gardez une vue claire de vos logements.
            </p>
          </div>

          <div className="rounded-xl border border-gray-200 p-6">
            <h2 className="font-medium text-gray-900">Locataires</h2>
            <p className="mt-2 text-sm text-gray-600">
              Retrouvez facilement les informations essentielles.
            </p>
          </div>

          <div className="rounded-xl border border-gray-200 p-6">
            <h2 className="font-medium text-gray-900">Paiements</h2>
            <p className="mt-2 text-sm text-gray-600">
              Suivez les loyers et les retards simplement.
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}