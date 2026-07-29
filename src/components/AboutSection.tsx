import { ArrowUpRight, Mail, MapPin } from "lucide-react";
import { forwardRef } from "react";
import { siteContent, type SectionId } from "../data/siteContent";

type AboutSectionProps = {
  onNavigate: (id: SectionId) => void;
};

export const AboutSection = forwardRef<HTMLElement, AboutSectionProps>(
  function AboutSection({ onNavigate }, ref) {
    const content = siteContent.about;

    return (
      <section id="about" ref={ref} className="about-hero">
        <div className="portrait-wrap">
          <img
            src={content.portrait.src}
            alt={content.portrait.alt}
            className="portrait-image"
          />
        </div>

        <div className="status-pill">
          <span className="status-dot" />
          {content.status}
        </div>

        <h1 className="about-title">{content.name}</h1>

        <div className="about-content">
          {content.groups.map((group) => (
            <div className="about-block" key={group.title}>
              <h2>{group.title}</h2>
              <ul>
                {group.details.map((detail, index) => (
                  <li key={index}>{detail}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="about-actions">
          <button
            className="primary-about-action"
            onClick={() => onNavigate("research")}
          >
            <ArrowUpRight size={17} />
            {content.actions.research}
          </button>

          <a
            className="secondary-about-action"
            href={content.actions.location.href}
            target="_blank"
            rel="noreferrer"
          >
            <MapPin size={17} />
            {content.actions.location.label}
          </a>

          <a
            className="secondary-about-action"
            href={content.actions.schoolPage.href}
            target="_blank"
            rel="noreferrer"
          >
            <ArrowUpRight size={17} />
            {content.actions.schoolPage.label}
          </a>

          <a
            className="secondary-about-action"
            href={content.actions.email.href}
          >
            <Mail size={17} />
            {content.actions.email.label}
          </a>

          <a
            className="secondary-about-action"
            href={content.actions.scholar.href}
            target="_blank"
            rel="noreferrer"
          >
            <ArrowUpRight size={17} />
            {content.actions.scholar.label}
          </a>
        </div>
      </section>
    );
  },
);
