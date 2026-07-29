import { forwardRef } from "react";
import { siteContent } from "../data/siteContent";

export const ServicesSection = forwardRef<HTMLElement>(
  function ServicesSection(_, ref) {
    const content = siteContent.services;

    return (
      <section id="services" ref={ref} className="services-section">
        <div className="section-kicker">
          <span>{content.sectionNumber}</span>
          <p>{content.sectionTitle}</p>
          <div />
        </div>

        <div className="services-content">
          {content.groups.map((group) => (
            <div className="services-block" key={group.title}>
              <h2>{group.title}</h2>
              <ul>
                {group.details.map((detail, index) => (
                  <li key={index}>{detail}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>
    );
  },
);
