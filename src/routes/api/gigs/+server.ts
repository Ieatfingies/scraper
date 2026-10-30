import { json } from '@sveltejs/kit';
import { SUPABASE_URL, SUPABASE_KEY } from '$env/static/private';

export async function GET() {
	try {
		const endpoint = `${SUPABASE_URL}?select=*&order=created.desc&limit=100`;
		const res = await fetch(endpoint, {
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