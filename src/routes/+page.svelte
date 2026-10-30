<script lang="ts">
	import { onMount } from 'svelte';

	interface Gig {
		id: string;
		title: string;
		link: string;
		subreddit: string;
		created: number;
	}

	let gigs: Gig[] = [];
	let loading = true;

	async function fetchGigs() {
		loading = true;
		try {
			const res = await fetch('/api/gigs');
			if (res.ok) {
				gigs = await res.json();
			}
		} catch (e) {
			console.error(e);
		} finally {
			loading = false;
		}
	}

	onMount(() => {
		fetchGigs();
	});

	function formatTime(timestamp: number) {
		if (!timestamp) return 'JUST NOW';
		const date = new Date(timestamp * 1000);
		return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
	}
</script>

<div class="page-wrapper">
	<main class="container">
		<header class="header">
			<div>
				<h1 class="title">GIG <span class="accent">SCRAPER</span></h1>
				<p class="subtitle">Live Reddit Opportunity Feed</p>
			</div>

			<button on:click={fetchGigs} disabled={loading} class="refresh-btn">
				{#if loading}
					<span class="spinner"></span> Refreshing...
				{:else}
					Refresh Feed
				{/if}
			</button>
		</header>

		{#if loading && gigs.length === 0}
			<div class="feed">
				{#each Array(4) as _}
					<div class="skeleton"></div>
				{/each}
			</div>
		{:else if gigs.length === 0}
			<div class="empty">
				<p>No matching gigs found right now.</p>
			</div>
		{:else}
			<div class="feed">
				{#each gigs as gig (gig.id)}
					<div class="card">
						<div class="card-body">
							<div class="meta">
								<span class="badge">r/{gig.subreddit}</span>
								<span class="time">{formatTime(gig.created)}</span>
							</div>
							<h2 class="gig-title">{gig.title}</h2>
						</div>

						<a href={gig.link} target="_blank" rel="noopener noreferrer" class="view-btn">
							View Task →
						</a>
					</div>
				{/each}
			</div>
		{/if}
	</main>
</div>

<style>
	:global(body) {
		margin: 0;
		padding: 0;
		background-color: #0f172a;
		color: #f8fafc;
		font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
	}

	.page-wrapper {
		min-height: 100vh;
		padding: 2.5rem 1rem;
		box-sizing: border-box;
	}

	.container {
		max-width: 900px;
		margin: 0 auto;
	}

	.header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		border-bottom: 1px solid #1e293b;
		padding-bottom: 1.5rem;
		margin-bottom: 2rem;
	}

	.title {
		margin: 0;
		font-size: 2rem;
		font-weight: 800;
		letter-spacing: -0.025em;
		color: #ffffff;
	}

	.accent {
		color: #ff4655;
	}

	.subtitle {
		margin: 0.25rem 0 0 0;
		font-size: 0.875rem;
		color: #94a3b8;
	}

	.refresh-btn {
		background-color: #ff4655;
		color: #ffffff;
		border: none;
		padding: 0.65rem 1.25rem;
		font-weight: 600;
		font-size: 0.875rem;
		border-radius: 6px;
		cursor: pointer;
		display: flex;
		align-items: center;
		gap: 0.5rem;
		transition: background-color 0.15s ease;
	}

	.refresh-btn:hover {
		background-color: #e03e4d;
	}

	.refresh-btn:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.feed {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.card {
		background-color: #1e293b;
		border: 1px solid #334155;
		border-radius: 8px;
		padding: 1.25rem 1.5rem;
		display: flex;
		flex-direction: column;
		gap: 1rem;
		justify-content: space-between;
		transition: border-color 0.15s ease, transform 0.15s ease;
	}

	@media (min-width: 640px) {
		.card {
			flex-direction: row;
			align-items: center;
		}
	}

	.card:hover {
		border-color: #ff4655;
		transform: translateY(-2px);
	}

	.meta {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		margin-bottom: 0.5rem;
	}

	.badge {
		font-size: 0.75rem;
		font-weight: 700;
		padding: 0.25rem 0.6rem;
		background-color: #0f172a;
		color: #ff4655;
		border-radius: 4px;
		border: 1px solid rgba(255, 70, 85, 0.2);
	}

	.time {
		font-size: 0.75rem;
		color: #94a3b8;
	}

	.gig-title {
		margin: 0;
		font-size: 1.05rem;
		font-weight: 600;
		color: #f8fafc;
		line-height: 1.4;
	}

	.view-btn {
		text-decoration: none;
		padding: 0.55rem 1rem;
		font-size: 0.85rem;
		font-weight: 600;
		color: #f8fafc;
		background-color: #0f172a;
		border-radius: 6px;
		border: 1px solid #334155;
		transition: background-color 0.15s ease, border-color 0.15s ease;
		white-space: nowrap;
		align-self: flex-start;
	}

	@media (min-width: 640px) {
		.view-btn {
			align-self: center;
		}
	}

	.view-btn:hover {
		background-color: #ff4655;
		border-color: #ff4655;
		color: #ffffff;
	}

	.skeleton {
		height: 80px;
		background-color: #1e293b;
		border-radius: 8px;
		opacity: 0.5;
	}

	.empty {
		text-align: center;
		padding: 4rem 1rem;
		border: 1px dashed #334155;
		border-radius: 8px;
		color: #94a3b8;
	}

	.spinner {
		display: inline-block;
		width: 14px;
		height: 14px;
		border: 2px solid rgba(255, 255, 255, 0.3);
		border-top-color: #ffffff;
		border-radius: 50%;
		animation: spin 0.8s linear infinite;
	}

	@keyframes spin {
		to { transform: rotate(360deg); }
	}
</style>