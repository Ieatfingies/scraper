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

<div class="val-app">
	<main class="main-container">
		<header class="header">
			<h1 class="title">
				GIG <span class="highlight">SCRAPER</span>
			</h1>

			<button on:click={fetchGigs} disabled={loading} class="btn-primary">
				<span class="btn-content">
					{#if loading}
						<span class="spinner"></span> REFRESHING...
					{:else}
						⚡ REFRESH FEED
					{/if}
				</span>
				<div class="sheen"></div>
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
				<p>NO GIGS FOUND</p>
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

						<a href={gig.link} target="_blank" rel="noopener noreferrer" class="btn-action">
							<span>VIEW TASK →</span>
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
		background-color: #0f1722;
		color: #f1f5f9;
		font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
	}

	.val-app {
		min-height: 100vh;
		padding: 2.5rem 1rem;
		box-sizing: border-box;
	}

	.main-container {
		max-width: 1000px;
		margin: 0 auto;
	}

	.header {
		display: flex;
		flex-direction: column;
		gap: 1rem;
		justify-content: space-between;
		align-items: flex-start;
		border-bottom: 2px solid #1e293b;
		padding-bottom: 1.5rem;
		margin-bottom: 2rem;
	}

	@media (min-width: 640px) {
		.header {
			flex-direction: row;
			align-items: center;
		}
	}

	.title {
		margin: 0;
		font-size: 2.5rem;
		font-weight: 900;
		font-style: italic;
		text-transform: uppercase;
		color: #ffffff;
		letter-spacing: -0.025em;
	}

	.highlight {
		color: #ff4655;
	}

	.btn-primary {
		position: relative;
		overflow: hidden;
		background-color: #ff4655;
		color: #ffffff;
		border: none;
		padding: 0.85rem 2rem;
		font-weight: 800;
		font-size: 0.85rem;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		cursor: pointer;
		transition: transform 0.15s ease, opacity 0.15s ease;
		clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px);
	}

	.btn-primary:active {
		transform: scale(0.96);
	}

	.btn-primary:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.btn-content {
		position: relative;
		z-index: 2;
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.sheen {
		position: absolute;
		inset: 0;
		background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
		transform: translateX(-100%);
		transition: transform 0.5s ease;
	}

	.btn-primary:hover .sheen {
		transform: translateX(100%);
	}

	.card-list {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.gig-card {
		background-color: #141e2d;
		border: 1px solid #1e293b;
		padding: 1.25rem 1.5rem;
		display: flex;
		flex-direction: column;
		gap: 1rem;
		justify-content: space-between;
		clip-path: polygon(12px 0, 100% 0, 100% calc(100% - 12px), calc(100% - 12px) 100%, 0 100%, 0 12px);
		transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
		animation: valEnter 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards;
		animation-delay: calc(var(--i) * 45ms);
		opacity: 0;
		transform: translateY(15px);
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
		box-shadow: 0 0 20px rgba(255, 70, 85, 0.25);
	}

	.meta-row {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		margin-bottom: 0.5rem;
	}

	.badge {
		font-size: 0.65rem;
		font-weight: 800;
		padding: 0.2rem 0.5rem;
		background-color: #1e293b;
		color: #ff4655;
		text-transform: uppercase;
		border: 1px solid rgba(255, 70, 85, 0.3);
	}

	.time {
		font-size: 0.75rem;
		color: #64748b;
	}

	.gig-title {
		margin: 0;
		font-size: 1.1rem;
		font-weight: 700;
		color: #f8fafc;
		line-height: 1.4;
	}

	.btn-action {
		align-self: flex-start;
		text-decoration: none;
		padding: 0.65rem 1.25rem;
		font-size: 0.75rem;
		font-weight: 900;
		letter-spacing: 0.1em;
		color: #f1f5f9;
		background-color: transparent;
		border: 1px solid #334155;
		clip-path: polygon(8px 0, 100% 0, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0 100%, 0 8px);
		transition: background-color 0.2s ease, border-color 0.2s ease, color 0.2s ease;
		white-space: nowrap;
	}

	@media (min-width: 640px) {
		.btn-action {
			align-self: center;
		}
	}

	.btn-action:hover {
		background-color: #ff4655;
		border-color: #ff4655;
		color: #ffffff;
	}

	.skeleton-card {
		height: 90px;
		background-color: #1e293b;
		opacity: 0.5;
		clip-path: polygon(12px 0, 100% 0, 100% calc(100% - 12px), calc(100% - 12px) 100%, 0 100%, 0 12px);
		animation: pulse 1.5s infinite ease-in-out;
	}

	.empty-state {
		text-align: center;
		padding: 4rem 1rem;
		border: 1px dashed #1e293b;
		color: #64748b;
		letter-spacing: 0.1em;
	}

	.spinner {
		display: inline-block;
		width: 12px;
		height: 12px;
		border: 2px solid rgba(255,255,255,0.3);
		border-top-color: #ffffff;
		border-radius: 50%;
		animation: spin 0.8s linear infinite;
	}

	@keyframes valEnter {
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