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

<div class="val-container">
	<div class="grid-bg"></div>

	<main class="main-wrapper">
		<header class="header">
			<div class="title-section">
				<h1 class="title">GIG <span class="accent">SCRAPER</span></h1>
			</div>

			<button on:click={fetchGigs} disabled={loading} class="val-btn">
				<span class="btn-text">
					{#if loading}
						<span class="spinner"></span> REFRESHING...
					{:else}
						⚡ REFRESH FEED
					{/if}
				</span>
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
				<p>NO GIGS DETECTED</p>
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

						<a href={gig.link} target="_blank" rel="noopener noreferrer" class="view-btn">
							VIEW TASK →
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
		color: #ece8e1;
		font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
	}

	.val-container {
		min-height: 100vh;
		padding: 2.5rem 1rem;
		position: relative;
		box-sizing: border-box;
	}

	.grid-bg {
		position: fixed;
		inset: 0;
		background-size: 30px 30px;
		background-image: 
			linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px),
			linear-gradient(to bottom, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
		pointer-events: none;
	}

	.main-wrapper {
		max-width: 950px;
		margin: 0 auto;
		position: relative;
		z-index: 10;
	}

	.header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		border-bottom: 2px solid #1f293d;
		padding-bottom: 1.25rem;
		margin-bottom: 2rem;
	}

	.title {
		margin: 0;
		font-size: 2.25rem;
		font-weight: 900;
		letter-spacing: -0.02em;
		color: #ffffff;
		font-style: italic;
	}

	.accent {
		color: #ff4655;
	}

	.val-btn {
		background-color: #ff4655;
		color: #ffffff;
		border: none;
		padding: 0.75rem 1.5rem;
		font-weight: 800;
		font-size: 0.8rem;
		letter-spacing: 0.05em;
		cursor: pointer;
		clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px);
		transition: transform 0.1s ease, background-color 0.15s ease;
	}

	.val-btn:hover {
		background-color: #e03e4d;
	}

	.val-btn:active {
		transform: scale(0.96);
	}

	.val-btn:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.btn-text {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.card-list {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.gig-card {
		background-color: #141e2d;
		border: 1px solid #1f293d;
		padding: 1.25rem 1.5rem;
		display: flex;
		flex-direction: column;
		gap: 1rem;
		justify-content: space-between;
		clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px);
		transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
		animation: slideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
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
		box-shadow: 0 0 15px rgba(255, 70, 85, 0.2);
	}

	.meta-row {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		margin-bottom: 0.5rem;
	}

	.badge {
		font-size: 0.7rem;
		font-weight: 800;
		padding: 0.2rem 0.5rem;
		background-color: #0f1722;
		color: #ff4655;
		border: 1px solid rgba(255, 70, 85, 0.3);
	}

	.time {
		font-size: 0.75rem;
		color: #7688a0;
	}

	.gig-title {
		margin: 0;
		font-size: 1.05rem;
		font-weight: 700;
		color: #ffffff;
		line-height: 1.4;
	}

	.view-btn {
		text-decoration: none;
		padding: 0.6rem 1.1rem;
		font-size: 0.75rem;
		font-weight: 800;
		letter-spacing: 0.05em;
		color: #ece8e1;
		background-color: #0f1722;
		border: 1px solid #2a384f;
		clip-path: polygon(6px 0, 100% 0, 100% calc(100% - 6px), calc(100% - 6px) 100%, 0 100%, 0 6px);
		transition: background-color 0.2s ease, border-color 0.2s ease, color 0.2s ease;
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

	.skeleton-card {
		height: 85px;
		background-color: #141e2d;
		clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px);
		animation: pulse 1.5s infinite ease-in-out;
	}

	.empty-state {
		text-align: center;
		padding: 4rem 1rem;
		border: 1px dashed #1f293d;
		color: #7688a0;
	}

	.spinner {
		display: inline-block;
		width: 12px;
		height: 12px;
		border: 2px solid rgba(255, 255, 255, 0.3);
		border-top-color: #ffffff;
		border-radius: 50%;
		animation: spin 0.8s linear infinite;
	}

	@keyframes slideIn {
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