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

<div class="app-container">
	<main class="main-content">
		<header class="header">
			<div class="title-group">
				<h1 class="title">GIG SCRAPER</h1>
				<p class="subtitle">Live Reddit job feed</p>
			</div>

			<button on:click={fetchGigs} disabled={loading} class="btn-refresh">
				{#if loading}
					<span class="spinner"></span> Refreshing...
				{:else}
					Refresh Feed
				{/if}
			</button>
		</header>

		{#if loading && gigs.length === 0}
			<div class="card-list">
				{#each Array(4) as _}
					<div class="skeleton-card"></div>
				{/each}
			</div>
		{:else if gigs.length === 0}
			<div class="empty-state">
				<p>No gigs found yet.</p>
			</div>
		{:else}
			<div class="card-list">
				{#each gigs as gig, i (gig.id)}
					<div style="--i: {i}" class="gig-card">
						<div class="gig-info">
							<div class="meta-row">
								<span class="badge">r/{gig.subreddit}</span>
								<span class="time">{formatTime(gig.created)}</span>
							</div>
							<h2 class="gig-title">{gig.title}</h2>
						</div>

						<a href={gig.link} target="_blank" rel="noopener noreferrer" class="btn-view">
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
		background-color: #0b0f19;
		color: #e2e8f0;
		font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
	}

	.app-container {
		min-height: 100vh;
		padding: 2.5rem 1rem;
		box-sizing: border-box;
	}

	.main-content {
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
		letter-spacing: -0.03em;
		color: #ffffff;
	}

	.subtitle {
		margin: 0.25rem 0 0 0;
		font-size: 0.875rem;
		color: #94a3b8;
	}

	.btn-refresh {
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
		transition: background-color 0.15s ease, transform 0.1s ease;
	}

	.btn-refresh:hover {
		background-color: #e03e4d;
	}

	.btn-refresh:active {
		transform: scale(0.97);
	}

	.btn-refresh:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.card-list {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.gig-card {
		background-color: #131b2e;
		border: 1px solid #1e293b;
		border-radius: 8px;
		padding: 1.25rem 1.5rem;
		display: flex;
		flex-direction: column;
		gap: 1rem;
		justify-content: space-between;
		transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
		animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
		animation-delay: calc(var(--i) * 35ms);
		opacity: 0;
		transform: translateY(12px);
	}

	@media (min-width: 640px) {
		.gig-card {
			flex-direction: row;
			align-items: center;
		}
	}

	.gig-card:hover {
		border-color: #ff4655;
		transform: translateY(-2px);
		box-shadow: 0 4px 20px rgba(255, 70, 85, 0.15);
	}

	.meta-row {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		margin-bottom: 0.5rem;
	}

	.badge {
		font-size: 0.75rem;
		font-weight: 700;
		padding: 0.25rem 0.6rem;
		background-color: #1e293b;
		color: #ff4655;
		border-radius: 4px;
	}

	.time {
		font-size: 0.75rem;
		color: #64748b;
	}

	.gig-title {
		margin: 0;
		font-size: 1.05rem;
		font-weight: 600;
		color: #f8fafc;
		line-height: 1.4;
	}

	.btn-view {
		text-decoration: none;
		padding: 0.55rem 1rem;
		font-size: 0.85rem;
		font-weight: 600;
		color: #e2e8f0;
		background-color: #1e293b;
		border-radius: 6px;
		border: 1px solid #334155;
		transition: background-color 0.2s ease, border-color 0.2s ease, color 0.2s ease;
		white-space: nowrap;
		align-self: flex-start;
	}

	@media (min-width: 640px) {
		.btn-view {
			align-self: center;
		}
	}

	.btn-view:hover {
		background-color: #ff4655;
		border-color: #ff4655;
		color: #ffffff;
	}

	.skeleton-card {
		height: 85px;
		background-color: #1e293b;
		border-radius: 8px;
		opacity: 0.5;
		animation: pulse 1.5s infinite ease-in-out;
	}

	.empty-state {
		text-align: center;
		padding: 4rem 1rem;
		border: 1px dashed #1e293b;
		border-radius: 8px;
		color: #64748b;
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

	@keyframes slideUp {
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	@keyframes pulse {
		0%, 100% { opacity: 0.3; }
		50% { opacity: 0.7; }
	}

	@keyframes spin {
		to { transform: rotate(360deg); }
	}
</style>