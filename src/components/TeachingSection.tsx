import { forwardRef } from "react";
import { siteContent } from "../data/siteContent";

export const TeachingSection = forwardRef<HTMLElement>(
  function TeachingSection(_, ref) {
    const content = siteContent.teaching;

    return (
      <section id="teaching" ref={ref} className="teaching-section">
        <div className="section-kicker">
          <span>{content.sectionNumber}</span>
          <p>{content.sectionTitle}</p>
          <div />
        </div>

        <div className="teaching-content">
          {content.groups.map((group) => (
            <div className="teaching-block" key={group.title}>
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
