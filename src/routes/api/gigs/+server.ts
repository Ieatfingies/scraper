import { json } from '@sveltejs/kit';

const SUPABASE_URL = 'https://lyofifkmhhlatybkqydl.supabase.co/rest/v1/gigs?select=*&order=created.desc&limit=100';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx5b2ZpZmttaGhsYXR5YmtxeWRsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTMzNjY0ODksImV4cCI6MjEwODk0MjQ4OX0.Va99aGzwS-tyUHyD61iMED2FZfv0FRcm5SPUQlsGZ3c';

export async function GET() {
	try {
		const res = await fetch(SUPABASE_URL, {
			headers: {
				'apikey': SUPABASE_KEY,
				'Authorization': `Bearer ${SUPABASE_KEY}`
			}
		});

		if (!res.ok) {
			return json([], { status: res.status });
		}

		const data = await res.json();
		return json(data);
	} catch (e) {
		return json([], { status: 500 });
	}
}