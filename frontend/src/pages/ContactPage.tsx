import { FormEvent, useState } from 'react';

const CONTACT_EMAIL = 'haxodrat@icloud.com';
const LINKEDIN_URL = 'https://www.linkedin.com/in/ckim259/';
const GITHUB_URL = 'https://github.com/Haxodrat';

export default function ContactPage() {
  const [name, setName] = useState('');
  const [senderEmail, setSenderEmail] = useState('');
  const [subject, setSubject] = useState('ValeSportsModel inquiry');
  const [message, setMessage] = useState('');

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const bodyLines = [
      `Name: ${name || 'N/A'}`,
      `Email: ${senderEmail || 'N/A'}`,
      '',
      message || '',
    ];

    const mailto = `mailto:${CONTACT_EMAIL}?subject=${encodeURIComponent(
      subject
    )}&body=${encodeURIComponent(bodyLines.join('\n'))}`;

    window.location.href = mailto;
  }

  return (
    <section className="page">
      <div className="page-header">
        <p className="eyebrow">Contact</p>
        <h2>About this project</h2>
        <p className="muted">
          ValeSportsModel is a Valorant esports app focused on upcoming VCT match
          predictions and regional Elo rankings.
        </p>
      </div>

      <div className="contact-grid">
        <div className="state-card">
          <h3 className="contact-card-title">Project overview</h3>
          <p className="muted">
            Built to compare teams across Pacific, EMEA, China, and Americas
            using a streamlined Elo baseline before adding richer machine
            learning models.
          </p>

          <div className="contact-links">
            <a
              href={`mailto:${CONTACT_EMAIL}`}
              className="contact-link"
            >
              {CONTACT_EMAIL}
            </a>

            <a
              href={LINKEDIN_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="contact-link"
            >
              LinkedIn
            </a>

            <a
              href={GITHUB_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="contact-link"
            >
              GitHub
            </a>
          </div>
        </div>

        <div className="state-card">
          <h3 className="contact-card-title">Send me a message</h3>

          <form className="contact-form" onSubmit={handleSubmit}>
            <label className="contact-label">
              Name
              <input
                className="contact-input"
                type="text"
                value={name}
                onChange={(event) => setName(event.target.value)}
                placeholder="Your name"
              />
            </label>

            <label className="contact-label">
              Your email
              <input
                className="contact-input"
                type="email"
                value={senderEmail}
                onChange={(event) => setSenderEmail(event.target.value)}
                placeholder="you@example.com"
              />
            </label>

            <label className="contact-label">
              Subject
              <input
                className="contact-input"
                type="text"
                value={subject}
                onChange={(event) => setSubject(event.target.value)}
                placeholder="Subject"
              />
            </label>

            <label className="contact-label">
              Message
              <textarea
                className="contact-input contact-textarea"
                value={message}
                onChange={(event) => setMessage(event.target.value)}
                placeholder="Write your message here"
                rows={6}
                required
              />
            </label>

            <button type="submit" className="contact-submit">
              Open email draft
            </button>
          </form>
        </div>
      </div>
    </section>
  );
}